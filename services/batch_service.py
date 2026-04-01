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
