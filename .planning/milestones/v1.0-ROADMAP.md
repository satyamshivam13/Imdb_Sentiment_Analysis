# Roadmap: IMDb Sentiment Analytics Platform

## Overview

This roadmap evolves the current sentiment predictor into an analytics-focused platform for stakeholder demos. Work starts with dependable data foundations, then layers in batch processing, dashboard insights, model transparency, and final UX hardening for repeatable showcase use.

## Phases

- [x] **Phase 1: Analytics Data Foundation** - Establish persistent analysis history and shared analytics primitives. (completed 2026-04-01)
- [x] **Phase 2: Batch CSV Analysis Pipeline** - Add validated CSV upload, multi-row scoring, and export/report outputs. (completed 2026-04-01)
- [x] **Phase 3: Dashboard Visualization Layer** - Deliver stakeholder-facing sentiment distribution and trend dashboards. (completed 2026-04-02)
- [x] **Phase 4: Model Metrics Observatory** - Expose evaluation metrics, confusion matrix, and model metadata. (completed 2026-04-02)
- [x] **Phase 5: History Experience Hardening** - Finalize history browsing/clearing UX and reliability/performance polish. (completed 2026-04-02)
- [ ] **Phase 6: Milestone Documentation Reconciliation** - Close audit-identified planning/documentation drift before archival. (planned 2026-04-02)

## Phase Details

### Phase 1: Analytics Data Foundation
**Goal**: Create a robust data layer for storing analysis events and feeding downstream analytics features.
**Depends on**: Nothing (first phase)
**Requirements**: HIST-01
**Success Criteria** (what must be TRUE):
1. Analyzed review events are persisted with timestamp, sentiment, and confidence.
2. Core analytics aggregation utilities exist and are reusable by batch/dashboard flows.
3. Persistence implementation includes migration/initialization path and basic integrity checks.
**Plans**: 3 plans

Plans:
- [x] 01-01: Introduce storage layer and schema for analysis events
- [x] 01-02: Add write/read integration for prediction endpoints
- [x] 01-03: Add foundational tests and data integrity guards

### Phase 2: Batch CSV Analysis Pipeline
**Goal**: Enable reliable multi-review analysis through validated CSV workflows and exportable outputs.
**Depends on**: Phase 1
**Requirements**: BATCH-01, BATCH-02, BATCH-03, BATCH-04, BATCH-05
**Success Criteria** (what must be TRUE):
1. Users can upload supported CSV files and receive clear validation feedback on bad input.
2. Each valid row is scored with sentiment and confidence.
3. Users can download enriched CSV output and view aggregate batch summary metrics.
**Plans**: 3 plans

Plans:
- [x] 02-01: Build CSV upload and schema validation flow
- [x] 02-02: Implement batch scoring pipeline with row-level outputs
- [x] 02-03: Add batch report summary and export endpoint/UI

### Phase 3: Dashboard Visualization Layer
**Goal**: Deliver dashboard visuals that communicate current sentiment landscape and trends over time.
**Depends on**: Phase 2
**Requirements**: DASH-01, DASH-02, DASH-03
**Success Criteria** (what must be TRUE):
1. Dashboard displays sentiment distribution with clear counts and percentages.
2. Trend chart visualizes sentiment over time from persisted history/batch data.
3. Date-range controls correctly filter chart outputs.
**Plans**: 3 plans

Plans:
- [x] 03-01: Add dashboard routes and data aggregation endpoints
- [x] 03-02: Integrate chart rendering for distribution and trends
- [x] 03-03: Implement date-range filtering and chart-state validation

### Phase 4: Model Metrics Observatory
**Goal**: Provide transparent model quality views that stakeholders can interpret confidently.
**Depends on**: Phase 3
**Requirements**: METR-01, METR-02, METR-03
**Success Criteria** (what must be TRUE):
1. Metrics panel shows accuracy, precision, recall, and F1 values from tracked evaluation artifacts.
2. Confusion matrix and class support values render accurately.
3. Model metadata (type/version/evaluated timestamp) is visible alongside metrics.
**Plans**: 2 plans

Plans:
- [x] 04-01: Add metrics artifact loader and summary API
- [x] 04-02: Build metrics page and confusion-matrix UI

### Phase 5: History Experience Hardening
**Goal**: Complete v1 usability by strengthening history navigation, clearing controls, and performance hygiene.
**Depends on**: Phase 4
**Requirements**: HIST-02, HIST-03
**Success Criteria** (what must be TRUE):
1. Users can browse history in chronological order with stable behavior.
2. Users can clear history safely and immediately see reflected state.
3. History and trend views remain responsive at expected demo dataset sizes.
**Plans**: 2 plans

Plans:
- [x] 05-01: Build paginated history browse page and retrieval support
- [x] 05-02: Add clear-history action and validation scaffolding

### Phase 6: Milestone Documentation Reconciliation
**Goal**: Reconcile milestone governance documents with implemented v1 reality so archival artifacts are accurate.
**Depends on**: Phase 5
**Requirements**: Documentation debt closure (no new product requirements)
**Gap Closure**: Closes debt from .planning/v1.0-MILESTONE-AUDIT.md
**Success Criteria** (what must be TRUE):
1. REQUIREMENTS traceability/checklists reflect implemented v1 completion state.
2. PROJECT current-state narrative matches completed milestone outcomes.
3. Milestone documentation is audit-consistent for archival.
**Plans**: 1 plan

Plans:
- [x] 06-01: Reconcile REQUIREMENTS and PROJECT milestone state

## Progress

**Execution Order:**
Phases execute in numeric order: 1 -> 2 -> 3 -> 4 -> 5 -> 6

| Phase | Plans Complete | Status | Completed |
|-------|----------------|--------|-----------|
| 1. Analytics Data Foundation | 3/3 | Complete | 2026-04-01 |
| 2. Batch CSV Analysis Pipeline | 3/3 | Complete | 2026-04-01 |
| 3. Dashboard Visualization Layer | 3/3 | Complete | 2026-04-02 |
| 4. Model Metrics Observatory | 2/2 | Complete | 2026-04-02 |
| 5. History Experience Hardening | 2/2 | Complete | 2026-04-02 |
| 6. Milestone Documentation Reconciliation | 0/1 | Planned | - |