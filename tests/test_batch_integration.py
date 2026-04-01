from __future__ import annotations

from io import BytesIO
from pathlib import Path
import re

import app as app_module
from services import BatchService, HistoryService
from storage.history_store import HistoryStore


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
            return [[0.1, 0.9]]
        return [[0.9, 0.1]]


def _configure_test_app(tmp_path: Path):
    db_path = tmp_path / "batch_integration.db"
    store = HistoryStore(db_path)
    store.init_schema()

    app_module.app.config["TESTING"] = True
    app_module.app.config["HISTORY_DB_PATH"] = str(db_path)
    app_module.history_store = store
    app_module.history_service = HistoryService(store)
    app_module.batch_service = BatchService()
    app_module.batch_export_cache.clear()
    app_module.vectorizer = DummyVectorizer()
    app_module.model = DummyModel()
    app_module.model_error = None
    return app_module.app.test_client(), store


def test_api_batch_analyze_returns_mixed_results_and_persists_rows(tmp_path: Path) -> None:
    client, store = _configure_test_app(tmp_path)
    csv_body = "review,title\nGreat movie,A\n,Missing review\n"

    response = client.post(
        "/api/batch/analyze",
        data={"reviews_file": (BytesIO(csv_body.encode("utf-8")), "batch.csv")},
    )
    assert response.status_code == 200

    payload = response.get_json()
    assert payload["status"] == "analyzed"
    assert payload["valid_rows"] == 1
    assert payload["invalid_rows"] == 1
    assert len(payload["scored_rows"]) == 1
    assert payload["summary"]["positive_count"] == 1
    assert payload["export_id"]
    assert payload["export_url"].startswith("/batch/export/")

    latest = store.latest_events(limit=5)
    assert len(latest) == 1
    assert latest[0]["source"] == "batch"


def test_batch_analyze_renders_result_and_export_download(tmp_path: Path) -> None:
    client, _store = _configure_test_app(tmp_path)
    csv_body = "review,title\nGreat movie,A\nBad movie,B\n"

    response = client.post(
        "/batch/analyze",
        data={"reviews_file": (BytesIO(csv_body.encode("utf-8")), "batch.csv")},
    )
    assert response.status_code == 200
    html = response.data.decode("utf-8")
    assert "Batch Analysis Report" in html

    match = re.search(r"/batch/export/([a-f0-9]+)", html)
    assert match is not None
    export_path = f"/batch/export/{match.group(1)}"

    export_response = client.get(export_path)
    assert export_response.status_code == 200
    assert "text/csv" in export_response.content_type
    exported_body = export_response.data.decode("utf-8")
    assert "sentiment_label,sentiment_value,confidence" in exported_body


def test_batch_analyze_returns_400_when_all_rows_invalid(tmp_path: Path) -> None:
    client, _store = _configure_test_app(tmp_path)
    csv_body = "review,title\n,Empty one\n,Empty two\n"

    response = client.post(
        "/batch/analyze",
        data={"reviews_file": (BytesIO(csv_body.encode("utf-8")), "batch.csv")},
    )
    assert response.status_code == 400
    html = response.data.decode("utf-8")
    assert "CSV row validation failed" in html
