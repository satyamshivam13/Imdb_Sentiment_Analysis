from __future__ import annotations

import json

import app as app_module
from services.metrics_service import MetricsArtifactError, MetricsService


EXPECTED_METRICS = {
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


class BrokenMetricsService:
    def load_metrics(self):
        raise MetricsArtifactError("Metrics artifact not available.")


def test_metrics_summary_endpoint_returns_artifact_contract():
    client = app_module.app.test_client()

    response = client.get("/api/metrics/summary")

    assert response.status_code == 200
    payload = response.get_json()
    assert set(payload.keys()) == {"summary", "confusion_matrix", "classes", "metadata"}
    assert payload == EXPECTED_METRICS


def test_metrics_service_normalizes_artifact_payload():
    service = MetricsService()

    payload = service.load_metrics()

    assert payload == EXPECTED_METRICS
    assert isinstance(payload["summary"]["accuracy"], float)
    assert payload["confusion_matrix"][0][0] == 214


def test_metrics_summary_endpoint_returns_error_when_artifact_is_missing(monkeypatch):
    monkeypatch.setattr(app_module, "metrics_service", BrokenMetricsService())
    client = app_module.app.test_client()

    response = client.get("/api/metrics/summary")

    assert response.status_code == 503
    payload = response.get_json()
    assert payload["error"] == "metrics_unavailable"
    assert "Metrics artifact not available" in payload["detail"]
