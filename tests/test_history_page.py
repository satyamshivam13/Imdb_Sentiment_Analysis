from __future__ import annotations

from pathlib import Path

import app as app_module


def _build_store(tmp_path: Path):
    store = app_module.HistoryStore(tmp_path / "history.db")
    store.init_schema()
    for index in range(1, 22):
        sentiment_label = "Positive" if index % 2 else "Negative"
        confidence = 0.9 if sentiment_label == "Positive" else 0.4
        source = "single" if index % 3 else "batch"
        store.insert_event(
            review_text=f"Review {index} with enough detail to identify ordering.",
            sentiment_label=sentiment_label,
            sentiment_value=1 if sentiment_label == "Positive" else 0,
            confidence=confidence,
            source=source,
            created_at=f"2026-04-{index:02d}T12:00:00Z",
        )
    return store


def test_history_page_renders_paginated_rows_and_navigation(tmp_path, monkeypatch):
    monkeypatch.setattr(app_module, "history_store", _build_store(tmp_path))
    client = app_module.app.test_client()

    response = client.get("/history")

    assert response.status_code == 200
    html = response.get_data(as_text=True)
    assert "Analysis History" in html
    assert "1 / 2" in html
    assert "Next" in html
    assert 'href="/history"' in html
    assert "Review 21 with enough detail to identify ordering." in html
    assert "Review 20 with enough detail to identify ordering." in html
    assert html.index("Review 21") < html.index("Review 20")
    assert "single" in html
    assert "batch" in html


def test_history_page_uses_previous_link_on_later_pages(tmp_path, monkeypatch):
    monkeypatch.setattr(app_module, "history_store", _build_store(tmp_path))
    client = app_module.app.test_client()

    response = client.get("/history?page=2")

    assert response.status_code == 200
    html = response.get_data(as_text=True)
    assert "2 / 2" in html
    assert "Previous" in html
    assert "Review 1 with enough detail to identify ordering." in html
    assert "Review 2 with enough detail to identify ordering." not in html
