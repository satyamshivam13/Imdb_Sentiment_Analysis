from __future__ import annotations

from pathlib import Path

import app as app_module


def _build_store(tmp_path: Path):
    store = app_module.HistoryStore(tmp_path / "history.db")
    store.init_schema()
    for index in range(1, 4):
        store.insert_event(
            review_text=f"Clearable review {index}",
            sentiment_label="Positive" if index % 2 else "Negative",
            sentiment_value=1 if index % 2 else 0,
            confidence=0.8,
            source="single",
            created_at=f"2026-04-0{index}T12:00:00Z",
        )
    return store


def test_history_clear_route_empties_store_and_redirects(tmp_path, monkeypatch):
    store = _build_store(tmp_path)
    monkeypatch.setattr(app_module, "history_store", store)
    client = app_module.app.test_client()

    response = client.post("/history/clear")

    assert response.status_code in {302, 308}
    assert response.headers["Location"].endswith("/history")
    assert store.count_events() == 0

    history_response = client.get("/history")
    assert history_response.status_code == 200
    assert "No history yet" in history_response.get_data(as_text=True)


def test_history_clear_route_rejects_get_requests(tmp_path, monkeypatch):
    monkeypatch.setattr(app_module, "history_store", _build_store(tmp_path))
    client = app_module.app.test_client()

    response = client.get("/history/clear")

    assert response.status_code == 405


def test_history_page_includes_clear_confirmation_control(tmp_path, monkeypatch):
    monkeypatch.setattr(app_module, "history_store", _build_store(tmp_path))
    client = app_module.app.test_client()

    response = client.get("/history")

    assert response.status_code == 200
    html = response.get_data(as_text=True)
    assert "Clear All History" in html
    assert "confirm('Clear all local history?')" in html
    assert 'action="/history/clear"' in html