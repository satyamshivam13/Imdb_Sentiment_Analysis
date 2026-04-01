# IMDb Sentiment Analytics Platform

## What This Is

This project evolves an existing IMDb sentiment prediction Flask app into an analytics-focused product for internal and demo stakeholders. Instead of showing only a single prediction, it surfaces sentiment patterns, model quality, and batch insights useful for presentations and decision discussions.

## Core Value

Internal stakeholders can quickly understand sentiment trends and model quality from review data, not just single-review outputs.

## Requirements

### Validated

- [x] User can submit one movie review and receive a sentiment classification in the web UI (existing `app.py` + `templates/` flow)
- [x] Client can call a JSON prediction API (`POST /api/predict`) for programmatic sentiment inference (existing)
- [x] System exposes model readiness health check (`GET /health`) for runtime verification (existing)
- [x] Results UI already displays classification and confidence context for a single review (existing)
- [x] System persists analyzed review events (timestamp, sentiment, confidence) for analytics foundations, validated in Phase 1 (`storage/history_store.py`, `services/history_service.py`, `app.py`)

### Active

- [ ] Analytics dashboard with sentiment distribution charts and sentiment-over-time trend views
- [ ] Model performance metrics panel (accuracy, precision, recall, F1, confusion matrix)
- [ ] Batch review analysis via CSV upload, multi-review scoring, and exportable results
- [ ] Review history and trend exploration without authentication (persistence foundation complete, user-facing history UX pending)

### Out of Scope

- User authentication and account management in v1, deferred to v2 to keep focus on analytics value
- Mobile app/PWA packaging in v1, web analytics experience is priority for current milestone
- Interactive API documentation page in v1, lower priority than analytics core
- Multi-model comparison and A/B benchmarking in v1, planned after baseline analytics workflows stabilize

## Context

- Existing codebase is a Flask monolith with Jinja templates and local ML artifacts (`Naive_Bayes_model_imdb.pkl`, `countVect_imdb.pkl`).
- Project includes polished UI patterns and a production entrypoint (`Procfile` with `gunicorn app:app`).
- Primary audience is internal/demo stakeholders, so visibility and explainability matter as much as raw prediction output.
- Codebase mapping identified a duplicate nested project structure (`Imdb-Sentiment-Analysis-Flask/`) and lack of automated tests, which informed sequencing.

## Constraints

- **Architecture**: Keep Flask backend and add a lightweight JavaScript chart stack (for example, Chart.js) without adding SPA complexity.
- **Scope Size**: Balanced v1 with 4 feature tracks, enough breadth for a complete analytics story while keeping delivery practical.
- **User Focus**: Optimize first for internal/demo stakeholders, prioritizing clarity, metrics visibility, and presentability.
- **Authentication**: Deferred from v1 to avoid non-core complexity.
- **Inference Runtime**: Maintain compatibility with existing local pickle-based inference artifacts.

## Key Decisions

| Decision | Rationale | Outcome |
|----------|-----------|---------|
| Analytics product is the v1 core value | Demonstrates higher ML product maturity than single prediction pages | Active |
| Primary user is internal/demo stakeholders | Existing artifacts indicate showcase/demo intent | Active |
| v1 scope is balanced (4 feature tracks) | Balances ship speed and narrative completeness | Active |
| Selected v1 features: Dashboard + Metrics + Batch CSV + Review History | Supports analytics storytelling and practical demos | In progress (Phase 1 complete) |
| Tech direction: Flask + lightweight JS charting | Delivers charts quickly without front-end architecture expansion | Active |
| Authentication deferred to v2 | Keeps v1 focused on core product value | Accepted |

## Current State

- Phase 1 complete: analytics data foundation implemented (persistent history store, service abstraction, and persistence wiring for web/API prediction routes).
- Phase 2 is next: batch CSV analysis pipeline.

## Evolution

This document evolves at phase transitions and milestone boundaries.

After each phase transition:
1. Move validated requirements to `Validated` with phase reference.
2. Move invalidated requirements to `Out of Scope` with reason.
3. Add newly discovered requirements to `Active`.
4. Record final decisions in `Key Decisions`.
5. Refresh `Current State`.

After each milestone:
1. Review all sections for drift.
2. Confirm Core Value is still the right priority.
3. Re-check Out of Scope reasons.
4. Update Context with latest architecture and delivery state.

---
*Last updated: 2026-04-02 after Phase 1 completion*
