# Phase 2: Batch CSV Analysis Pipeline - Discussion Log

> **Audit trail only.** Do not use as input to planning, research, or execution agents.
> Decisions are captured in `02-CONTEXT.md`; this log preserves alternatives considered.

**Date:** 2026-04-02
**Phase:** 2-batch-csv-analysis-pipeline
**Areas discussed:** CSV input contract, validation strategy, processing mode, export/report format
**Mode note:** Non-interactive fallback used in this runtime; recommended defaults were selected.

---

## CSV Input Contract

| Option | Description | Selected |
|--------|-------------|----------|
| Strict `review` only | Require one exact column name; simplest validator | |
| Canonical + aliases | Accept `review` plus common aliases, normalize to `review` | yes |
| Fully dynamic mapping | User maps arbitrary columns in UI/API | |

**User choice:** Canonical + aliases (recommended default in non-interactive fallback)
**Notes:** Balances compatibility with predictable downstream processing.

---

## Validation Strategy

| Option | Description | Selected |
|--------|-------------|----------|
| Fail-fast file-level | Abort entire file on first schema/row error | |
| Mixed-result processing | Score valid rows, report invalid rows with actionable errors | yes |
| Silent skip invalid rows | Ignore invalid rows with minimal feedback | |

**User choice:** Mixed-result processing (recommended default in non-interactive fallback)
**Notes:** Directly supports BATCH-02 and BATCH-03 while preserving demo reliability.

---

## Processing Mode

| Option | Description | Selected |
|--------|-------------|----------|
| Synchronous bounded processing | Process in request lifecycle with size/row limits | yes |
| Asynchronous queued processing | Background jobs with polling/webhooks | |
| Hybrid mode | Small files sync, large files async | |

**User choice:** Synchronous bounded processing (recommended default in non-interactive fallback)
**Notes:** Fits current Flask architecture and v1 delivery speed.

---

## Export and Report Format

| Option | Description | Selected |
|--------|-------------|----------|
| Enriched CSV + summary metrics | Append sentiment fields and return aggregate counts/percentages | yes |
| JSON-only report | Structured JSON output without downloadable CSV | |
| Multiple export formats | CSV + XLSX + JSON in v1 | |

**User choice:** Enriched CSV + summary metrics (recommended default in non-interactive fallback)
**Notes:** Aligns with BATCH-04/BATCH-05 and stakeholder demo expectations.

---

## Agent's Discretion

- Export file storage/streaming mechanism.
- Exact response envelopes for HTML vs API endpoints.
- Minor UX copy and interaction details for batch upload and results.

## Deferred Ideas

- Background job queue for large-batch async execution.
- XLSX/parquet imports.
- Persisted multi-run batch management UI.
