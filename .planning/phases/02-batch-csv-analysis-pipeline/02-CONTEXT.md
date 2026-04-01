# Phase 2: Batch CSV Analysis Pipeline - Context

**Gathered:** 2026-04-02
**Status:** Ready for planning

<domain>
## Phase Boundary

Phase 2 delivers reliable multi-review CSV analysis in the existing Flask app: upload CSV, validate input with actionable feedback, score valid rows, and provide exportable analyzed results plus summary metrics.
This phase does not add auth, model comparison, or dashboard visual analytics.

</domain>

<decisions>
## Implementation Decisions

### CSV Input Contract
- **D-01:** Accept `.csv` uploads only for v1, with UTF-8/UTF-8-SIG decoding support.
- **D-02:** Require a canonical text column named `review`; accept a small alias set (`reviews`, `review_text`, `text`) and normalize to `review` during validation.
- **D-03:** Enforce practical safety limits in v1 (request size and row-count guardrails) so batch processing remains synchronous and predictable for demo use.

### Validation and Error Behavior
- **D-04:** Use row-level validation with actionable diagnostics (`row`, `field`, `reason`) instead of fail-silent behavior.
- **D-05:** Process valid rows even when some rows fail validation, and return both analyzed output and validation issues in one result.
- **D-06:** If no rows are valid after validation, return a clear validation failure response and do not produce export artifacts.

### Processing and Persistence
- **D-07:** Keep v1 processing synchronous (no queue/background worker) to fit current Flask monolith and demo workflows.
- **D-08:** Reuse existing inference path semantics (`predict_sentiment`) for each valid row to keep single-review and batch-review outputs consistent.
- **D-09:** Persist successful batch row analyses into history with source tagging (`batch`) so downstream dashboard/history phases can reuse one data substrate.

### Export and Report UX
- **D-10:** Produce an enriched CSV export that appends sentiment fields (`sentiment_label`, `sentiment_value`, `confidence`) to original row data.
- **D-11:** Provide aggregate report metrics (positive/negative totals and percentages, valid/invalid counts) in the same batch result flow.
- **D-12:** Keep the first UX iteration lightweight: upload form + result summary + download action, aligned with current server-rendered app patterns.

### Agent's Discretion
- File lifecycle strategy for generated exports (in-memory stream vs short-lived temp file).
- Exact alias list expansion beyond the initial required set if research finds strong compatibility wins.
- Response shape details for HTML vs JSON surfaces, as long as requirement-level behavior remains intact.

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Scope and requirements
- `.planning/ROADMAP.md` - Phase 2 goal, dependencies, and success criteria.
- `.planning/REQUIREMENTS.md` - BATCH-01 through BATCH-05 requirement contract.
- `.planning/PROJECT.md` - product constraints, audience, and v1 scope guardrails.

### Existing persistence foundation from Phase 1
- `.planning/phases/01-analytics-data-foundation/01-VERIFICATION.md` - validated history foundation and quality gates.
- `storage/history_store.py` - persistence schema and query primitives used by downstream phases.
- `services/history_service.py` - service abstraction for writing analysis events.

### Existing app integration surfaces
- `app.py` - current routes, validation helpers, inference flow, and error patterns.
- `templates/home.html` - primary UI entry point likely to host batch upload controls.
- `static/js/app.js` - current client-side interaction pattern for form UX.

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- `predict_sentiment` in `app.py`: single place for sentiment prediction behavior and confidence derivation.
- `validate_review` in `app.py`: existing text validation semantics to mirror/extend for per-row batch checks.
- `HistoryService.append_prediction_event`: existing event persistence API to extend with `source="batch"`.
- `HistoryStore` (`insert_event`, `count_by_sentiment`, `trend_by_day`, `latest_events`): analytics-ready storage base already in place.

### Established Patterns
- Flask monolith with paired HTML/API routing style.
- Explicit error payload/status handling for JSON endpoints and user-friendly errors in templates.
- Minimal frontend JS enhancements layered onto server-rendered templates.

### Integration Points
- Add batch routes and processing helpers in `app.py` first (current architecture standard).
- Add upload/result controls in existing template flow (`templates/home.html` and/or dedicated batch result template).
- Extend `static/js/app.js` only for lightweight UX behaviors (file selection feedback, submit status, validation hints).

</code_context>

<specifics>
## Specific Ideas

- Keep stakeholder demo clarity high: emphasize row counts, failure reasons, and quick download path over advanced controls.
- Report validation errors with precise row references to reduce confusion during demos.
- Keep Phase 2 output contracts straightforward so Phase 3 dashboards can consume persisted data without rework.

</specifics>

<deferred>
## Deferred Ideas

- Async/background job orchestration for very large files.
- XLSX/parquet multi-format ingest.
- Saved batch history browser with user/session ownership semantics.

None of the above should be folded into Phase 2 implementation scope.

</deferred>

---

*Phase: 02-batch-csv-analysis-pipeline*
*Context gathered: 2026-04-02*
