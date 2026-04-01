# Phase 2 Research: Batch CSV Analysis Pipeline

**Phase:** 2 - Batch CSV Analysis Pipeline
**Date:** 2026-04-02
**Requirement IDs:** BATCH-01, BATCH-02, BATCH-03, BATCH-04, BATCH-05
**Confidence:** HIGH

## Objective

Research how to implement robust CSV batch sentiment analysis in the current Flask monolith while preserving existing prediction behavior and leveraging Phase 1 persistence primitives.

## User Constraints (from 02-CONTEXT.md)

### Locked Decisions

- Accept `.csv` only for v1 with UTF-8/UTF-8-SIG decoding support.
- Canonical text column is `review` with alias normalization from `reviews`, `review_text`, and `text`.
- Apply practical request size and row count limits for synchronous processing.
- Return actionable row-level validation errors and mixed-result outputs (valid rows processed, invalid rows reported).
- Keep processing synchronous for v1.
- Reuse `predict_sentiment` behavior per row.
- Persist successful batch row analyses with source `batch`.
- Provide enriched CSV export plus aggregate summary metrics.

### Agent's Discretion

- Export lifecycle strategy (in-memory or temporary file).
- Additional optional aliases beyond the required set.
- Final response envelope shape for HTML and API surfaces.

### Deferred (Out of Scope)

- Async/background job execution.
- XLSX/parquet ingestion.
- Multi-run batch management UI.

## Findings

### Ingestion and Validation

- Python standard library `csv` is sufficient for v1 and keeps dependency footprint stable.
- `io.TextIOWrapper` plus UTF-8/UTF-8-SIG decoding cleanly handles common Excel-export CSVs.
- A two-stage validation model is appropriate:
  - file-level checks (extension, size, required column presence)
  - row-level checks (missing/empty review, over max chars)

### Processing Pattern

- Build a dedicated batch service layer so route code remains readable:
  - parse and normalize rows
  - validate rows
  - run `predict_sentiment` for valid rows
  - persist valid results through `HistoryService`
  - compute summary metrics and export payload
- Keep deterministic order by preserving source row index and including it in outputs.

### Persistence and Analytics Compatibility

- Reusing `HistoryService.append_prediction_event(..., source="batch")` aligns batch and single-review data.
- Persist only successfully scored rows.
- Invalid rows should never produce history events.

### Export and Response Design

- Enriched CSV should include original columns plus `sentiment_label`, `sentiment_value`, and `confidence`.
- Summary metrics should include:
  - `total_rows`, `valid_rows`, `invalid_rows`
  - `positive_count`, `negative_count`
  - `positive_pct`, `negative_pct`
- Keep API-friendly JSON response shape and pair with HTML result rendering for demo stakeholders.

## Recommended Architecture

1. Add `services/batch_service.py` for parsing, validation, scoring, and result shaping.
2. Add `utils/csv_utils.py` for CSV normalization helpers and export generation.
3. Add batch endpoints in `app.py`:
   - HTML upload + results flow
   - API batch endpoint returning JSON diagnostics and download token/path
4. Add UI updates in `templates/home.html` (or dedicated batch template) plus minimal JS enhancement in `static/js/app.js`.

## Risks and Mitigations

| Risk | Impact | Mitigation |
|------|--------|------------|
| Large upload blocks request lifecycle | High | enforce row/file limits and explicit user feedback |
| Schema ambiguity from varied CSV headers | Medium | alias normalization + clear missing-column error |
| Partial failures confuse users | Medium | include row-indexed diagnostics and clear valid/invalid counts |
| Drift between single and batch predictions | Medium | reuse shared `predict_sentiment` path |
| Export mismatch with UI/API output | Medium | centralize export mapping in one helper |

## Validation Architecture

Phase 2 should include executable checks for:

- CSV upload acceptance and schema validation behavior.
- Mixed-result processing where valid rows are scored and invalid rows are reported.
- Persistence behavior for valid batch rows using source `batch`.
- Export payload correctness (expected columns present).
- Aggregate summary metrics correctness.

Minimum automated strategy:

- Unit tests for CSV normalization and validation helpers.
- Service-level tests for mixed-result pipeline and summary calculations.
- Integration tests for batch endpoint success/failure behavior.

## Recommended Plan Breakdown

1. Build CSV upload interface, file guards, and schema/row validation primitives.
2. Implement scoring pipeline plus persistence and mixed-result output contracts.
3. Deliver aggregate reporting + enriched export and validate through tests.

## Phase Output Expectations

- Users can upload supported CSV files and get actionable validation feedback.
- Valid rows are scored consistently with existing single-review logic.
- Users can access aggregate metrics and download enriched analyzed CSV outputs.

---
*Research complete for Phase 2*
