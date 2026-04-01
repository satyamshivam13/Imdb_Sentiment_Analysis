# IMDb Sentiment Analytics Platform

## What This Is

A Flask-based sentiment analytics platform that goes beyond single-review inference by presenting sentiment patterns, batch outcomes, model quality, and review history for internal stakeholder demos.

## Core Value

Internal stakeholders can quickly understand sentiment trends and model quality from review data, not just single-review outputs.

## Requirements

### Validated

- [x] User can submit one movie review and receive a sentiment classification in the web UI (`/predict`).
- [x] Client can call a JSON prediction API (`POST /api/predict`) for programmatic sentiment inference.
- [x] System exposes model readiness health check (`GET /health`) for runtime verification.
- [x] Results UI displays classification and confidence context for single-review output.
- [x] System persists analyzed review events (timestamp, sentiment, confidence).
- [x] System supports batch CSV upload, schema validation, row-level scoring, aggregate reporting, and enriched CSV export.
- [x] Dashboard surfaces sentiment distribution and trend with date-range controls (`/dashboard`).
- [x] Metrics observatory surfaces accuracy, precision, recall, F1, confusion matrix, and model metadata (`/metrics`).
- [x] History page supports chronological browsing and destructive clear flow (`/history`, `POST /history/clear`).

### Active

- [ ] v2 authentication and user-owned analytics history (`AUTH-01`, `AUTH-02`).
- [ ] Interactive API docs experience (`DOCS-01`).
- [ ] Multi-model comparison workflows (`MCOMP-01`).
- [ ] Mobile/PWA packaging (`MOB-01`).

### Out of Scope

- Auth/account management in v1 (deferred to v2 milestone).
- API explorer in v1 (deferred behind core analytics capabilities).
- Multi-model benchmarking in v1 (deferred until baseline analytics stabilization).
- Mobile app/PWA in v1 (web-first stakeholder delivery).

## Context

- Architecture remains a Flask monolith with server-rendered Jinja templates and lightweight JavaScript for interactive analytics views.
- Inference remains compatible with local pickle artifacts (`Naive_Bayes_model_imdb.pkl`, `countVect_imdb.pkl`).
- The platform now includes dedicated dashboard, metrics, batch, and history surfaces aligned for demo storytelling.
- Automated regression coverage is present via pytest and currently passes end-to-end.

## Constraints

- Keep Flask backend plus lightweight charting approach without introducing SPA complexity.
- Prioritize clarity and metrics visibility for internal/demo stakeholders.
- Preserve compatibility with existing local inference artifacts.
- Keep auth and multi-tenant history out of v1 scope.

## Key Decisions

| Decision | Rationale | Outcome |
|----------|-----------|---------|
| Keep Flask + server-rendered pages | Minimize complexity while increasing analytics capability | Active |
| Ship balanced v1 across four tracks (history foundation, batch, dashboard, metrics) | Provide complete analytics story for demos | Completed |
| Use precomputed metrics artifact for observability | Deterministic payload and stable contracts | Active |
| Keep history clear behavior destructive/simple in v1 | Match no-auth local-scope constraints | Active |
| Use implementation evidence as reconciliation source-of-truth | Resolve governance drift for milestone closeout | Active |

## Current State

- Phase 1 complete: analytics data foundation and persistence primitives.
- Phase 2 complete: batch CSV pipeline, mixed-result scoring, export and report outputs.
- Phase 3 complete: dashboard distribution/trend visualization and date-range controls.
- Phase 4 complete: model metrics API + dedicated metrics page with artifact-backed contracts.
- Phase 5 complete: history browse and clear flows with regression coverage.
- Phase 6 in progress: documentation reconciliation for milestone archival readiness.

## Evolution

This file updates at phase transitions and milestone boundaries:

1. Move shipped requirements into Validated.
2. Keep next-milestone items in Active.
3. Keep explicit deferrals in Out of Scope.
4. Record key decisions with outcomes.
5. Refresh Current State to match execution reality.

---
*Last updated: 2026-04-02 during Phase 6 reconciliation*