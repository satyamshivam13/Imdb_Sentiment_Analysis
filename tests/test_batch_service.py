from __future__ import annotations

from services.batch_service import BatchService


def _predict(review: str) -> dict:
    lowered = review.lower()
    is_positive = "great" in lowered or "good" in lowered
    if is_positive:
        return {"label": "Positive", "value": 1, "confidence": 0.91}
    return {"label": "Negative", "value": 0, "confidence": 0.13}


def test_normalize_review_column_accepts_aliases() -> None:
    service = BatchService()
    headers = ["id", "review_text", "genre"]
    selected = service.normalize_review_column(headers)
    assert selected == "review_text"


def test_analyze_rows_supports_mixed_validity_and_scoring() -> None:
    service = BatchService()
    rows = [
        {
            "row_index": 2,
            "review": "Great acting and direction",
            "original_row": {"review": "Great acting and direction", "title": "A"},
        },
        {
            "row_index": 3,
            "review": "",
            "original_row": {"review": "", "title": "B"},
        },
    ]

    result = service.analyze_rows(rows, _predict, max_chars=2000)

    assert result["valid_rows"] == 1
    assert result["invalid_rows"] == 1
    assert len(result["issues"]) == 1
    assert result["issues"][0]["row"] == 3
    assert result["issues"][0]["field"] == "review"

    assert len(result["scored_rows"]) == 1
    scored = result["scored_rows"][0]
    assert scored["row_index"] == 2
    assert scored["sentiment_label"] == "Positive"
    assert scored["sentiment_value"] == 1
    assert isinstance(scored["confidence"], float)
    assert scored["original_row"]["title"] == "A"


def test_analyze_rows_includes_confidence_and_label_fields() -> None:
    service = BatchService()
    rows = [
        {
            "row_index": 2,
            "review": "Bad pacing",
            "original_row": {"review": "Bad pacing"},
        }
    ]

    result = service.analyze_rows(rows, _predict, max_chars=2000)
    scored = result["scored_rows"][0]

    assert "sentiment_label" in scored
    assert "sentiment_value" in scored
    assert "confidence" in scored
    assert scored["sentiment_label"] == "Negative"
