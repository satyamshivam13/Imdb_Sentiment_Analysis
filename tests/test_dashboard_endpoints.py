from __future__ import annotations

from datetime import date, datetime, timedelta, timezone
from types import SimpleNamespace

import app as app_module


class DummyHistoryStore:
    def __init__(self, counts=None, trend_rows=None):
        self.counts = counts or []
        self.trend_rows = trend_rows or []
        self.count_args = []
        self.trend_args = []

    def count_by_sentiment(self, start_ts=None, end_ts=None):
        self.count_args.append((start_ts, end_ts))
        return self.counts

    def trend_by_day(self, start_ts=None, end_ts=None):
        self.trend_args.append((start_ts, end_ts))
        return self.trend_rows


class DummyResponse:
    def __init__(self, response, status_code=200):
        self._response = response
        self.status_code = status_code

    def get_json(self):
        return self._response.get_json()



def _install_history_store(monkeypatch, counts=None, trend_rows=None):
    dummy_store = DummyHistoryStore(counts=counts, trend_rows=trend_rows)
    monkeypatch.setattr(app_module, "history_store", dummy_store)
    return dummy_store



def test_distribution_payload_counts_and_percentages(monkeypatch):
    dummy_store = _install_history_store(
        monkeypatch,
        counts=[
            {"sentiment_label": "Positive", "total": 6},
            {"sentiment_label": "Negative", "total": 2},
        ],
    )
    client = app_module.app.test_client()

    response = client.get("/api/dashboard/distribution?range=30d")

    assert response.status_code == 200
    payload = response.get_json()
    assert payload["range_key"] == "30d"
    assert payload["total"] == 8
    assert payload["positive"]["count"] == 6
    assert payload["positive"]["percentage"] == 75.0
    assert payload["negative"]["count"] == 2
    assert payload["negative"]["percentage"] == 25.0
    assert dummy_store.count_args[0][0] is not None
    assert dummy_store.count_args[0][1] is not None



def test_trend_payload_has_aligned_series(monkeypatch):
    _install_history_store(
        monkeypatch,
        trend_rows=[
            {"day": "2026-04-01", "sentiment_label": "Positive", "total": 3},
            {"day": "2026-04-01", "sentiment_label": "Negative", "total": 1},
            {"day": "2026-04-03", "sentiment_label": "Positive", "total": 2},
        ],
    )
    client = app_module.app.test_client()

    response = client.get("/api/dashboard/trend?start=2026-04-01&end=2026-04-03")

    assert response.status_code == 200
    payload = response.get_json()
    assert payload["labels"] == ["2026-04-01", "2026-04-02", "2026-04-03"]
    assert payload["series"]["positive"] == [3, 0, 2]
    assert payload["series"]["negative"] == [1, 0, 0]



def test_date_range_filters_are_inclusive(monkeypatch):
    dummy_store = _install_history_store(monkeypatch, counts=[], trend_rows=[])
    client = app_module.app.test_client()

    response = client.get("/api/dashboard/distribution?start=2026-04-01&end=2026-04-01")

    assert response.status_code == 200
    start_ts, end_ts = dummy_store.count_args[0]
    assert start_ts == "2026-04-01T00:00:00+00:00"
    assert end_ts == "2026-04-02T00:00:00+00:00"



def test_dashboard_page_renders_empty_state(monkeypatch):
    dummy_store = _install_history_store(monkeypatch, counts=[], trend_rows=[])
    client = app_module.app.test_client()

    response = client.get("/dashboard")

    assert response.status_code == 200
    html = response.get_data(as_text=True)
    assert "Dashboard" in html
    assert "Try a broader date range" in html
    assert "Analyze another review" in html
    assert dummy_store.count_args
