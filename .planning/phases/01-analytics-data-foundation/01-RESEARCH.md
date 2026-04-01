# Phase 1 Research: Analytics Data Foundation

**Phase:** 1 - Analytics Data Foundation
**Date:** 2026-04-02
**Requirement IDs:** HIST-01
**Confidence:** HIGH

## Objective

Research how to implement durable analysis-event persistence and reusable aggregation primitives in the current Flask codebase with minimal architectural disruption.

## Findings

### Persistence Approach

- The current app has no database layer; introducing a lightweight local store is required.
- SQLite is the best fit for v1:
  - No additional infrastructure
  - Good enough for demo/stakeholder scale
  - Easy to query for dashboard and trend aggregations

### Data Contract for `HIST-01`

Recommended analysis event fields:
- `id` (integer primary key)
- `review_text` (text)
- `sentiment_label` (text, `Positive|Negative`)
- `sentiment_value` (integer, `1|0`)
- `confidence` (real nullable)
- `source` (text, `single|batch`)
- `created_at` (UTC timestamp)

### Integration Pattern

Use a service abstraction to avoid locking routes directly to storage:
- `storage/history_store.py` for CRUD and query helpers
- `services/history_service.py` for domain-level operations
- Route handlers call service methods after prediction completion

### Reusable Analytics Primitives

Create utility methods that downstream phases will consume:
- `count_by_sentiment(start_ts=None, end_ts=None)`
- `trend_by_day(start_ts=None, end_ts=None)`
- `latest_events(limit, offset)`

### Migration and Initialization

- Initialize schema automatically on app startup if missing.
- Keep schema in SQL file or explicit migration helper for reproducibility.
- Avoid silent schema drift by checking required columns at initialization.

## Risks and Mitigations

| Risk | Impact | Mitigation |
|------|--------|------------|
| Duplicate app copies diverge on persistence logic | High | Implement in root app only and document canonical path |
| Large review text bloats store quickly | Medium | Keep retention controls for later phases |
| Timestamp inconsistency | Medium | Normalize to UTC at write-time |

## Validation Architecture

The phase should ship with executable checks for:
- Schema initialization correctness
- Event write path after `/predict` and `/api/predict`
- Query helper correctness for counts and trends

Minimum automated strategy:
- Add focused tests for store initialization and insert/query behaviors.
- Add one integration-level test covering prediction -> persistence flow.

## Recommended Plan Breakdown

1. Introduce storage schema and repository/service abstraction.
2. Integrate persistence writes into prediction pathways.
3. Add tests and integrity guards for schema + query paths.

## Phase Output Expectations

- Persistent analysis events are available for future dashboard phases.
- Aggregation primitives are callable without route-level data logic duplication.
- Foundation is stable enough for Phase 2 batch ingestion integration.

---
*Research complete for Phase 1*
