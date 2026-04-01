# IMDb Sentiment Analytics Platform

## What This Is

This project evolves an existing IMDb sentiment prediction Flask app into an analytics-focused product for internal and demo stakeholders. Instead of showing only a single prediction, it will surface sentiment patterns, model quality, and batch insights that are useful for presentations and decision discussions.

## Core Value

Internal stakeholders can quickly understand sentiment trends and model quality from review data, not just single-review outputs.

## Requirements

### Validated

- ? User can submit one movie review and receive a sentiment classification in the web UI — existing (`app.py` + `templates/` flow)
- ? Client can call a JSON prediction API (`POST /api/predict`) for programmatic sentiment inference — existing
- ? System exposes model readiness health check (`GET /health`) for runtime verification — existing
- ? Results UI already displays classification and confidence context for a single review — existing

### Active

- [ ] Analytics dashboard with sentiment distribution charts and sentiment-over-time trend views
- [ ] Model performance metrics panel (accuracy, precision, recall, F1, confusion matrix)
- [ ] Batch review analysis via CSV upload, multi-review scoring, and exportable results
- [ ] Review history and trend exploration without authentication (session/local persistence)

### Out of Scope

- User authentication and account management in v1 — deferred to v2 to keep focus on analytics value
- Mobile app/PWA packaging in v1 — web analytics experience is priority for current milestone
- Interactive API documentation page in v1 — useful but lower priority than analytics core
- Multi-model comparison and A/B benchmarking in v1 — planned after baseline analytics workflows stabilize

## Context

- Existing codebase is a Flask monolith with Jinja templates and local ML artifacts (`Naive_Bayes_model_imdb.pkl`, `countVect_imdb.pkl`).
- Current project already includes polished UI patterns and a production entrypoint (`Procfile` with `gunicorn app:app`).
- Primary audience is internal/demo stakeholders, so visibility and explainability matter as much as raw prediction output.
- Codebase mapping identified duplicate project structure (`Imdb-Sentiment-Analysis-Flask/` nested copy) and lack of automated tests, which should inform sequencing.

## Constraints

- **Architecture**: Keep Flask backend and add a lightweight JavaScript chart stack (e.g., Chart.js) — chosen to increase capability without introducing SPA complexity.
- **Scope Size**: Balanced v1 with 4 feature tracks — enough breadth for a complete analytics story while keeping delivery practical.
- **User Focus**: Optimize first for internal/demo stakeholders — prioritize clarity, metrics visibility, and presentability.
- **Authentication**: Explicitly deferred from v1 — avoid non-core complexity while analytics foundation is built.
- **Inference Runtime**: Maintain compatibility with existing local pickle-based inference artifacts — preserve current prediction pipeline continuity.

## Key Decisions

| Decision | Rationale | Outcome |
|----------|-----------|---------|
| Analytics product is the v1 core value | Demonstrates higher ML product maturity than single prediction pages | — Pending |
| Primary user is internal/demo stakeholders | Existing artifacts indicate showcase/demo intent | — Pending |
| v1 scope is balanced (4 feature tracks) | Balances ship speed and narrative completeness | — Pending |
| Selected v1 features: Dashboard + Metrics + Batch CSV + Review History | Directly supports analytics storytelling and practical demos | — Pending |
| Tech direction: Flask + lightweight JS charting | Delivers charts quickly without front-end architecture expansion | — Pending |
| Authentication deferred to v2 | Keeps v1 focused on core product value | — Pending |

## Evolution

This document evolves at phase transitions and milestone boundaries.

**After each phase transition** (via `$gsd-transition`):
1. Requirements invalidated? ? Move to Out of Scope with reason
2. Requirements validated? ? Move to Validated with phase reference
3. New requirements emerged? ? Add to Active
4. Decisions to log? ? Add to Key Decisions
5. "What This Is" still accurate? ? Update if drifted

**After each milestone** (via `$gsd-complete-milestone`):
1. Full review of all sections
2. Core Value check — still the right priority?
3. Audit Out of Scope — reasons still valid?
4. Update Context with current state

---
*Last updated: 2026-04-02 after initialization*
