from __future__ import annotations

from pathlib import Path

from services.history_service import HistoryService
from storage.history_store import HistoryStore
import app as app_module


class DummyVectorizer:
    def transform(self, values):
        return values


class DummyModel:
    def predict(self, values):
        text = (values[0] or "").lower()
        return [1 if "great" in text or "good" in text else 0]

    def predict_proba(self, values):
        prediction = self.predict(values)[0]
        if prediction == 1:
            return [[0.05, 0.95]]
        return [[0.92, 0.08]]


def _configure_test_app(tmp_path: Path):
    db_path = tmp_path / "integration_history.db"
    store = HistoryStore(db_path)
    store.init_schema()

    app_module.app.config["TESTING"] = True
    app_module.app.config["HISTORY_DB_PATH"] = str(db_path)
    app_module.history_store = store
    app_module.history_service = HistoryService(store)
    app_module.vectorizer = DummyVectorizer()
    app_module.model = DummyModel()
    app_module.model_error = None
    return app_module.app.test_client(), store


def test_predict_route_persists_single_source_event(tmp_path: Path) -> None:
    client, store = _configure_test_app(tmp_path)

    response = client.post("/predict", data={"Reviews": "Great movie and soundtrack"})
    assert response.status_code == 200

    latest = store.latest_events(limit=1)
    assert len(latest) == 1
    assert latest[0]["source"] == "single"
    assert latest[0]["sentiment_label"] == "Positive"


def test_api_predict_route_persists_api_source_event(tmp_path: Path) -> None:
    client, store = _configure_test_app(tmp_path)

    response = client.post("/api/predict", json={"review": "Good acting and pacing"})
    assert response.status_code == 200
    payload = response.get_json()
    assert payload["label"] in {"Positive", "Negative"}

    latest = store.latest_events(limit=1)
    assert len(latest) == 1
    assert latest[0]["source"] == "api"


def test_api_bad_request_does_not_persist_event(tmp_path: Path) -> None:
    client, store = _configure_test_app(tmp_path)

    response = client.post("/api/predict", json={"review": ""})
    assert response.status_code == 400
    assert store.latest_events(limit=10) == []
