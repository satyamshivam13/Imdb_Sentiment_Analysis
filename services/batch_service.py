from __future__ import annotations

import csv
from io import StringIO
from pathlib import Path
from typing import Any


class BatchService:
    REVIEW_ALIASES = ("review", "reviews", "review_text", "text")

    def parse_csv_upload(self, file_storage: Any) -> dict[str, Any]:
        issues: list[dict[str, Any]] = []
        if file_storage is None:
            issues.append(
                {"row": 0, "field": "reviews_file", "reason": "CSV file is required."}
            )
            return {"filename": "", "headers": [], "rows": [], "issues": issues}

        filename = (getattr(file_storage, "filename", "") or "").strip()
        if not filename:
            issues.append(
                {"row": 0, "field": "reviews_file", "reason": "CSV file is required."}
            )
            return {"filename": "", "headers": [], "rows": [], "issues": issues}

        if Path(filename).suffix.lower() != ".csv":
            issues.append(
                {
                    "row": 0,
                    "field": "reviews_file",
                    "reason": "Only .csv files are supported.",
                }
            )
            return {"filename": filename, "headers": [], "rows": [], "issues": issues}

        raw_bytes = file_storage.read() or b""
        if not raw_bytes:
            issues.append(
                {
                    "row": 0,
                    "field": "reviews_file",
                    "reason": "Uploaded CSV is empty.",
                }
            )
            return {"filename": filename, "headers": [], "rows": [], "issues": issues}

        try:
            decoded = raw_bytes.decode("utf-8-sig")
        except UnicodeDecodeError:
            issues.append(
                {
                    "row": 0,
                    "field": "reviews_file",
                    "reason": "CSV must be UTF-8 encoded.",
                }
            )
            return {"filename": filename, "headers": [], "rows": [], "issues": issues}

        reader = csv.DictReader(StringIO(decoded))
        headers = [header for header in (reader.fieldnames or []) if header is not None]
        if not headers:
            issues.append(
                {
                    "row": 0,
                    "field": "schema",
                    "reason": "CSV header row is missing.",
                }
            )
            return {"filename": filename, "headers": [], "rows": [], "issues": issues}

        review_column = self.normalize_review_column(headers)
        if review_column is None:
            issues.append(
                {
                    "row": 0,
                    "field": "review",
                    "reason": (
                        "Missing review column. Use one of: "
                        "review, reviews, review_text, text."
                    ),
                }
            )
            return {
                "filename": filename,
                "headers": headers,
                "rows": [],
                "issues": issues,
            }

        rows: list[dict[str, Any]] = []
        for row_index, row in enumerate(reader, start=2):
            original_row: dict[str, str] = {}
            for key, value in row.items():
                if key is None:
                    continue
                original_row[key] = (value or "").strip()
            rows.append(
                {
                    "row_index": row_index,
                    "review": original_row.get(review_column, ""),
                    "original_row": original_row,
                }
            )

        if not rows:
            issues.append(
                {
                    "row": 0,
                    "field": "rows",
                    "reason": "CSV has no data rows.",
                }
            )

        return {
            "filename": filename,
            "headers": headers,
            "rows": rows,
            "issues": issues,
            "review_column": review_column,
        }

    def normalize_review_column(self, fieldnames: list[str]) -> str | None:
        normalized = {(name or "").strip().lower(): name for name in fieldnames}
        for alias in self.REVIEW_ALIASES:
            if alias in normalized:
                return normalized[alias]
        return None

    def validate_rows(
        self, rows: list[dict[str, Any]], max_chars: int
    ) -> dict[str, list[dict[str, Any]]]:
        valid_rows: list[dict[str, Any]] = []
        issues: list[dict[str, Any]] = []

        for row in rows:
            row_index = int(row.get("row_index", 0))
            review = (row.get("review", "") or "").strip()
            if not review:
                issues.append(
                    {
                        "row": row_index,
                        "field": "review",
                        "reason": "Review text is empty.",
                    }
                )
                continue
            if len(review) > max_chars:
                issues.append(
                    {
                        "row": row_index,
                        "field": "review",
                        "reason": f"Review exceeds max length ({max_chars}).",
                    }
                )
                continue

            valid_rows.append(
                {
                    "row_index": row_index,
                    "review": review,
                    "original_row": dict(row.get("original_row", {})),
                }
            )

        return {"valid_rows": valid_rows, "issues": issues}

    def analyze_rows(self, rows, predict_fn, max_chars: int) -> dict[str, Any]:
        validation = self.validate_rows(rows, max_chars)
        valid_rows = validation["valid_rows"]
        issues = list(validation["issues"])
        scored_rows: list[dict[str, Any]] = []

        for row in valid_rows:
            review_text = row["review"]
            try:
                prediction = predict_fn(review_text)
            except Exception as exc:
                issues.append(
                    {
                        "row": row["row_index"],
                        "field": "prediction",
                        "reason": f"Prediction failed: {type(exc).__name__}",
                    }
                )
                continue

            scored_rows.append(
                {
                    "row_index": row["row_index"],
                    "review": review_text,
                    "sentiment_label": prediction["label"],
                    "sentiment_value": int(prediction["value"]),
                    "confidence": prediction["confidence"],
                    "original_row": dict(row["original_row"]),
                }
            )

        return {
            "valid_rows": len(scored_rows),
            "invalid_rows": len(issues),
            "scored_rows": scored_rows,
            "issues": issues,
        }

    def build_summary(
        self, scored_rows: list[dict[str, Any]], invalid_rows: int | list[dict[str, Any]]
    ) -> dict[str, Any]:
        invalid_count = (
            len(invalid_rows) if isinstance(invalid_rows, list) else int(invalid_rows)
        )
        valid_count = len(scored_rows)
        total_rows = valid_count + invalid_count
        positive_count = sum(
            1 for row in scored_rows if row.get("sentiment_label") == "Positive"
        )
        negative_count = sum(
            1 for row in scored_rows if row.get("sentiment_label") == "Negative"
        )

        def pct(part: int, whole: int) -> float:
            if whole <= 0:
                return 0.0
            return round((part / whole) * 100, 1)

        return {
            "total_rows": total_rows,
            "valid_rows": valid_count,
            "invalid_rows": invalid_count,
            "positive_count": positive_count,
            "negative_count": negative_count,
            "positive_pct": pct(positive_count, valid_count),
            "negative_pct": pct(negative_count, valid_count),
        }

    def build_enriched_csv(
        self, original_headers: list[str], scored_rows: list[dict[str, Any]]
    ) -> str:
        export_headers = list(original_headers)
        for extra in ("sentiment_label", "sentiment_value", "confidence"):
            if extra not in export_headers:
                export_headers.append(extra)

        stream = StringIO()
        writer = csv.DictWriter(stream, fieldnames=export_headers)
        writer.writeheader()

        for row in scored_rows:
            original_row = dict(row.get("original_row", {}))
            export_row = {header: original_row.get(header, "") for header in original_headers}
            export_row["sentiment_label"] = row.get("sentiment_label", "")
            export_row["sentiment_value"] = row.get("sentiment_value", "")
            confidence = row.get("confidence")
            export_row["confidence"] = "" if confidence is None else confidence
            writer.writerow(export_row)

        return stream.getvalue()
