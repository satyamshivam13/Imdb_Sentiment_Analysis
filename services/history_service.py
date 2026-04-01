from __future__ import annotations

from storage import HistoryStore


class HistoryService:
    def __init__(self, store: HistoryStore):
        self.store = store

    def append_prediction_event(
        self,
        review_text: str,
        label: str,
        value: int,
        confidence: float | None,
        source: str,
    ) -> int:
        return self.store.insert_event(
            review_text=review_text,
            sentiment_label=label,
            sentiment_value=value,
            confidence=confidence,
            source=source,
        )
