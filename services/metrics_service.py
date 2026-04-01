from __future__ import annotations

import json
from pathlib import Path
from typing import Any

BASE_DIR = Path(__file__).resolve().parent.parent
DEFAULT_METRICS_PATH = BASE_DIR / "data" / "model_metrics.json"
REQUIRED_SUMMARY_KEYS = ("accuracy", "precision", "recall", "f1")
REQUIRED_METADATA_KEYS = ("model_type", "artifact_version", "evaluated_at")


class MetricsArtifactError(ValueError):
    pass


class MetricsService:
    def __init__(self, artifact_path: Path | str | None = None):
        self.artifact_path = Path(artifact_path or DEFAULT_METRICS_PATH).resolve()

    def load_metrics(self) -> dict[str, Any]:
        try:
            raw_payload = json.loads(self.artifact_path.read_text(encoding="utf-8"))
        except FileNotFoundError as exc:
            raise MetricsArtifactError(
                f"Metrics artifact not found: {self.artifact_path}"
            ) from exc
        except json.JSONDecodeError as exc:
            raise MetricsArtifactError(
                f"Metrics artifact is not valid JSON: {self.artifact_path}"
            ) from exc

        return self._normalize_payload(raw_payload)

    def _normalize_payload(self, payload: Any) -> dict[str, Any]:
        if not isinstance(payload, dict):
            raise MetricsArtifactError("Metrics artifact must be a JSON object.")

        summary = self._normalize_summary(payload.get("summary"))
        confusion_matrix = self._normalize_confusion_matrix(payload.get("confusion_matrix"))
        classes = self._normalize_classes(payload.get("classes"))
        metadata = self._normalize_metadata(payload.get("metadata"))

        return {
            "summary": summary,
            "confusion_matrix": confusion_matrix,
            "classes": classes,
            "metadata": metadata,
        }

    def _normalize_summary(self, summary: Any) -> dict[str, float]:
        if not isinstance(summary, dict):
            raise MetricsArtifactError("Metrics artifact summary must be an object.")

        normalized_summary: dict[str, float] = {}
        for key in REQUIRED_SUMMARY_KEYS:
            if key not in summary:
                raise MetricsArtifactError(f"Metrics artifact missing summary field: {key}")
            normalized_summary[key] = float(summary[key])
        return normalized_summary

    def _normalize_confusion_matrix(self, confusion_matrix: Any) -> list[list[int]]:
        if not isinstance(confusion_matrix, list) or len(confusion_matrix) != 2:
            raise MetricsArtifactError("Metrics artifact confusion_matrix must contain two rows.")

        normalized_matrix: list[list[int]] = []
        for row in confusion_matrix:
            if not isinstance(row, list) or len(row) != 2:
                raise MetricsArtifactError(
                    "Metrics artifact confusion_matrix rows must contain two values."
                )
            normalized_matrix.append([int(value) for value in row])
        return normalized_matrix

    def _normalize_classes(self, classes: Any) -> list[str]:
        if not isinstance(classes, list) or len(classes) != 2:
            raise MetricsArtifactError("Metrics artifact classes must contain exactly two labels.")
        normalized_classes = [str(label) for label in classes]
        if not all(normalized_classes):
            raise MetricsArtifactError("Metrics artifact class labels must be non-empty strings.")
        return normalized_classes

    def _normalize_metadata(self, metadata: Any) -> dict[str, str]:
        if not isinstance(metadata, dict):
            raise MetricsArtifactError("Metrics artifact metadata must be an object.")

        normalized_metadata = {}
        for key in REQUIRED_METADATA_KEYS:
            if key not in metadata:
                raise MetricsArtifactError(f"Metrics artifact missing metadata field: {key}")
            normalized_metadata[key] = str(metadata[key])

        for key, value in metadata.items():
            if key not in normalized_metadata:
                normalized_metadata[key] = str(value)
        return normalized_metadata
