from __future__ import annotations

from io import BytesIO
from werkzeug.datastructures import FileStorage

from services.batch_service import BatchService


def _upload(name: str, content: str) -> FileStorage:
    return FileStorage(
        stream=BytesIO(content.encode("utf-8")),
        filename=name,
        content_type="text/csv",
    )


def test_parse_csv_accepts_review_alias_and_extracts_rows() -> None:
    service = BatchService()
    upload = _upload(
        "reviews.csv",
        "review_text,title\nGreat movie,Alpha\nBad ending,Beta\n",
    )

    parsed = service.parse_csv_upload(upload)

    assert parsed["issues"] == []
    assert parsed["review_column"] == "review_text"
    assert len(parsed["rows"]) == 2
    assert parsed["rows"][0]["review"] == "Great movie"


def test_parse_csv_rejects_missing_review_column() -> None:
    service = BatchService()
    upload = _upload("reviews.csv", "headline,title\nGreat movie,Alpha\n")

    parsed = service.parse_csv_upload(upload)

    assert parsed["rows"] == []
    assert parsed["issues"]
    assert "Missing review column" in parsed["issues"][0]["reason"]


def test_validate_rows_flags_empty_and_overlong_reviews() -> None:
    service = BatchService()
    rows = [
        {"row_index": 2, "review": "", "original_row": {"review": ""}},
        {
            "row_index": 3,
            "review": "x" * 25,
            "original_row": {"review": "x" * 25},
        },
        {
            "row_index": 4,
            "review": "short valid review",
            "original_row": {"review": "short valid review"},
        },
    ]

    validated = service.validate_rows(rows, max_chars=20)

    assert len(validated["issues"]) == 2
    assert validated["issues"][0]["row"] == 2
    assert validated["issues"][1]["row"] == 3
    assert len(validated["valid_rows"]) == 1
    assert validated["valid_rows"][0]["row_index"] == 4
