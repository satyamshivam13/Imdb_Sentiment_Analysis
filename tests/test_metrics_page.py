from __future__ import annotations

import app as app_module


class DummyMetricsService:
    def __init__(self, payload):
        self.payload = payload

    def load_metrics(self):
        return self.payload


PAGE_PAYLOAD = {
    "summary": {
        "accuracy": 0.814,
        "precision": 0.8167,
        "recall": 0.8142,
        "f1": 0.8136,
    },
    "confusion_matrix": [[214, 35], [58, 193]],
    "classes": ["Negative", "Positive"],
    "metadata": {
        "model_type": "Naive Bayes sentiment classifier",
        "artifact_version": "v1.0.0",
        "evaluated_at": "2026-04-02T00:00:00Z",
        "source": "IMDB Reviews NLP.ipynb",
    },
}


def test_metrics_page_renders_headline_sections(monkeypatch):
    monkeypatch.setattr(app_module, "metrics_service", DummyMetricsService(PAGE_PAYLOAD))
    client = app_module.app.test_client()

    response = client.get("/metrics")

    assert response.status_code == 200
    html = response.get_data(as_text=True)
    assert "Metrics Observatory" in html
    assert "metrics-scorecards" in html
    assert "confusion-matrix" in html
    assert "model-metadata" in html
    assert "Accuracy" in html
    assert "Precision" in html
    assert "Recall" in html
    assert "F1" in html
    assert "Naive Bayes sentiment classifier" in html


def test_metrics_page_links_are_present_in_shell(monkeypatch):
    monkeypatch.setattr(app_module, "metrics_service", DummyMetricsService(PAGE_PAYLOAD))
    client = app_module.app.test_client()

    response = client.get("/metrics")

    assert response.status_code == 200
    html = response.get_data(as_text=True)
    assert "href=\"/metrics\"" in html
    assert "href=\"/dashboard\"" in html
    assert "Sentiment Studio" in html
