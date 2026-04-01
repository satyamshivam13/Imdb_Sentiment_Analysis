from __future__ import annotations

from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path
import sqlite3
from typing import Iterator


class HistoryStore:
    def __init__(self, db_path: str | Path):
        self.db_path = Path(db_path).resolve()
        self.db_path.parent.mkdir(parents=True, exist_ok=True)

    @contextmanager
    def _connect(self) -> Iterator[sqlite3.Connection]:
        connection = sqlite3.connect(self.db_path)
        connection.row_factory = sqlite3.Row
        try:
            yield connection
        finally:
            connection.close()

    def init_schema(self) -> None:
        with self._connect() as connection:
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS analysis_events (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    review_text TEXT NOT NULL,
                    sentiment_label TEXT NOT NULL,
                    sentiment_value INTEGER NOT NULL,
                    confidence REAL,
                    source TEXT NOT NULL,
                    created_at TEXT NOT NULL
                )
                """
            )
            connection.commit()

    def insert_event(
        self,
        review_text: str,
        sentiment_label: str,
        sentiment_value: int,
        confidence: float | None,
        source: str,
        created_at: str | None = None,
    ) -> int:
        created = created_at or datetime.now(timezone.utc).isoformat()
        with self._connect() as connection:
            cursor = connection.execute(
                """
                INSERT INTO analysis_events (
                    review_text, sentiment_label, sentiment_value, confidence, source, created_at
                )
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    review_text,
                    sentiment_label,
                    sentiment_value,
                    confidence,
                    source,
                    created,
                ),
            )
            connection.commit()
            return int(cursor.lastrowid)

    def count_by_sentiment(
        self, start_ts: str | None = None, end_ts: str | None = None
    ) -> list[dict]:
        query = """
            SELECT sentiment_label, COUNT(*) AS total
            FROM analysis_events
        """
        conditions = []
        values: list[str] = []
        if start_ts:
            conditions.append("created_at >= ?")
            values.append(start_ts)
        if end_ts:
            conditions.append("created_at <= ?")
            values.append(end_ts)
        if conditions:
            query += " WHERE " + " AND ".join(conditions)
        query += " GROUP BY sentiment_label ORDER BY sentiment_label"

        with self._connect() as connection:
            rows = connection.execute(query, values).fetchall()
        return [
            {"sentiment_label": row["sentiment_label"], "total": int(row["total"])}
            for row in rows
        ]

    def trend_by_day(
        self, start_ts: str | None = None, end_ts: str | None = None
    ) -> list[dict]:
        query = """
            SELECT DATE(created_at) AS day, sentiment_label, COUNT(*) AS total
            FROM analysis_events
        """
        conditions = []
        values: list[str] = []
        if start_ts:
            conditions.append("created_at >= ?")
            values.append(start_ts)
        if end_ts:
            conditions.append("created_at <= ?")
            values.append(end_ts)
        if conditions:
            query += " WHERE " + " AND ".join(conditions)
        query += " GROUP BY day, sentiment_label ORDER BY day ASC, sentiment_label ASC"

        with self._connect() as connection:
            rows = connection.execute(query, values).fetchall()
        return [
            {
                "day": row["day"],
                "sentiment_label": row["sentiment_label"],
                "total": int(row["total"]),
            }
            for row in rows
        ]

    def latest_events(self, limit: int = 50, offset: int = 0) -> list[dict]:
        with self._connect() as connection:
            rows = connection.execute(
                """
                SELECT
                    id,
                    review_text,
                    sentiment_label,
                    sentiment_value,
                    confidence,
                    source,
                    created_at
                FROM analysis_events
                ORDER BY created_at DESC
                LIMIT ? OFFSET ?
                """,
                (limit, offset),
            ).fetchall()
        return [dict(row) for row in rows]
