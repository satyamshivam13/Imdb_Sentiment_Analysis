from __future__ import annotations

import app as app_module


class DummyHistoryStore:
    def __init__(self, counts=None, trend_rows=None):
        self.counts = counts or []
        self.trend_rows = trend_rows or []

    def count_by_sentiment(self, start_ts=None, end_ts=None):
        return self.counts

    def trend_by_day(self, start_ts=None, end_ts=None):
        return self.trend_rows



def test_dashboard_page_includes_controls_and_chart_mounts(monkeypatch):
    monkeypatch.setattr(
        app_module,
        "history_store",
        DummyHistoryStore(
            counts=[
                {"sentiment_label": "Positive", "total": 4},
                {"sentiment_label": "Negative", "total": 1},
            ],
            trend_rows=[
                {"day": "2026-04-01", "sentiment_label": "Positive", "total": 4},
                {"day": "2026-04-01", "sentiment_label": "Negative", "total": 1},
            ],
        ),
    )
    client = app_module.app.test_client()

    response = client.get("/dashboard")

    assert response.status_code == 200
    html = response.get_data(as_text=True)
    assert "dashboard-controls" in html
    assert "dashboard-kpis" in html
    assert "distribution-chart" in html
    assert "trend-chart" in html
    assert "Quick ranges" in html
    assert "Apply" in html
    assert "Sentiment Distribution" in html
    assert "Sentiment Trend" in html



def test_dashboard_page_mentions_empty_state_guidance(monkeypatch):
    monkeypatch.setattr(
        app_module,
        "history_store",
        DummyHistoryStore(counts=[], trend_rows=[]),
    )
    client = app_module.app.test_client()

    response = client.get("/dashboard")

    assert response.status_code == 200
    html = response.get_data(as_text=True)
    assert "Try a broader date range" in html
    assert "prediction" in html.lower()
    assert "batch" in html.lower()
