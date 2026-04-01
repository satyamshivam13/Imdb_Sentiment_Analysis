from __future__ import annotations

from pathlib import Path
import sqlite3

from storage.history_store import HistoryStore


def _store(tmp_path: Path) -> HistoryStore:
    db_path = tmp_path / "history_test.db"
    store = HistoryStore(db_path)
    store.init_schema()
    return store


def test_init_schema_is_idempotent(tmp_path: Path) -> None:
    store = _store(tmp_path)
    store.init_schema()
    store.init_schema()

    con = sqlite3.connect(store.db_path)
    cur = con.cursor()
    cur.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name='analysis_events'"
    )
    row = cur.fetchone()
    con.close()
    assert row is not None


def test_insert_event_and_count_by_sentiment(tmp_path: Path) -> None:
    store = _store(tmp_path)
    store.insert_event("great movie", "Positive", 1, 0.91, "single")
    store.insert_event("bad movie", "Negative", 0, 0.87, "api")
    store.insert_event("solid movie", "Positive", 1, 0.66, "api")

    counts = store.count_by_sentiment()
    by_label = {entry["sentiment_label"]: entry["total"] for entry in counts}

    assert by_label["Positive"] == 2
    assert by_label["Negative"] == 1


def test_trend_by_day_groups_rows(tmp_path: Path) -> None:
    store = _store(tmp_path)
    store.insert_event(
        "first",
        "Positive",
        1,
        0.8,
        "single",
        created_at="2026-04-01T10:00:00+00:00",
    )
    store.insert_event(
        "second",
        "Negative",
        0,
        0.7,
        "api",
        created_at="2026-04-01T11:00:00+00:00",
    )
    store.insert_event(
        "third",
        "Positive",
        1,
        0.6,
        "api",
        created_at="2026-04-02T09:00:00+00:00",
    )

    trends = store.trend_by_day()
    keyed = {(item["day"], item["sentiment_label"]): item["total"] for item in trends}

    assert keyed[("2026-04-01", "Negative")] == 1
    assert keyed[("2026-04-01", "Positive")] == 1
    assert keyed[("2026-04-02", "Positive")] == 1
