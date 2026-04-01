# Project Research Summary

**Project:** IMDb Sentiment Analytics Platform
**Domain:** Sentiment analytics web application
**Researched:** 2026-04-02
**Confidence:** HIGH

## Executive Summary

The strongest path is to evolve the existing Flask sentiment predictor into an analytics-first experience without introducing a new frontend framework. This keeps delivery fast while materially increasing stakeholder value through trend visibility, batch analysis, and transparent model metrics.

The recommended architecture is a service-oriented Flask monolith: route handlers remain thin while analytics, batch processing, metrics, and history persistence move into focused modules. This directly supports the chosen v1 features and reduces risk from the current single-file backend pattern.

Primary risks are CSV validation drift, stale metric provenance, and data lineage mismatches in dashboard aggregates. Roadmap sequencing should address persistence and validation before heavy dashboard polish.

## Key Findings

### Recommended Stack

- Flask + Jinja templates remain fit-for-purpose for v1.
- Chart.js is sufficient for dashboard and trend visualizations.
- pandas should power CSV batch workflows.
- scikit-learn metrics should be surfaced from explicit artifacts tied to model version.

### Expected Features

**Must have (v1):**
- Dashboard distribution and trend charts
- Model metrics + confusion matrix
- Batch CSV upload and export
- Review history trend view (no auth)

**Defer (v2+):**
- Authentication
- API documentation explorer
- Multi-model comparison
- Mobile/PWA packaging

### Architecture Approach

Split core concerns into services: inference, batch, analytics, metrics, and history storage. Keep deployment simple (`gunicorn app:app`) while improving internals for testability and phase-by-phase delivery.

### Critical Pitfalls

1. Untrusted chart aggregates due to weak data lineage
2. CSV schema validation gaps causing inaccurate reports
3. Stale model metrics not tied to artifact versions
4. History trend performance degrading with growth

## Implications for Roadmap

### Phase 1: Foundation and History Data Model
**Rationale:** Dashboard and trend features require reliable persisted events and normalized timestamps.
**Delivers:** History storage abstraction and aggregation groundwork.

### Phase 2: Batch CSV Analysis Pipeline
**Rationale:** Batch ingestion unlocks large-sample analytics and reporting value early.
**Delivers:** Upload, validate, score, aggregate, and export flows.

### Phase 3: Analytics Dashboard Visualizations
**Rationale:** Stakeholder-facing value becomes visible once data pipelines are stable.
**Delivers:** Sentiment distribution and trend charts.

### Phase 4: Model Metrics Observatory
**Rationale:** Trust and explainability layer after dashboard core exists.
**Delivers:** Accuracy/precision/recall/F1 plus confusion matrix and model metadata.

### Phase 5: History Experience and Hardening
**Rationale:** Consolidate review history UX and address scale/performance concerns.
**Delivers:** Refined history explorer, filtering, and reliability improvements.

## Confidence Assessment

| Area | Confidence | Notes |
|------|------------|-------|
| Stack | HIGH | Strong match to existing codebase and constraints |
| Features | HIGH | Directly aligned with user decisions |
| Architecture | HIGH | Service extraction path is low-risk and incremental |
| Pitfalls | MEDIUM | Known risks; exact impact depends on data volume |

**Overall confidence:** HIGH

## Gaps to Address

- Decide canonical history persistence strategy (SQLite vs file-backed store) in Phase 1 planning.
- Define metric artifact generation and refresh workflow in Phase 4 planning.

---
*Research completed: 2026-04-02*
*Ready for roadmap: yes*
