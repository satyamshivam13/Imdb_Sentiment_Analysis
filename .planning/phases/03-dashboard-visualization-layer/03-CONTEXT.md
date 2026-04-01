# Phase 3: Dashboard Visualization Layer - Context

**Gathered:** 2026-04-02
**Status:** Ready for planning

<domain>
## Phase Boundary

Phase 3 delivers a stakeholder-facing dashboard experience that visualizes sentiment distribution and sentiment trend over time from persisted analysis events, with date-range filtering controls.
This phase is visualization-focused and does not add model metrics panels, authentication, or advanced segmentation workflows.

</domain>

<decisions>
## Implementation Decisions

### Dashboard Placement and Hierarchy
- **D-01:** Use a dedicated `/dashboard` route with a standalone dashboard page instead of embedding charts into the crowded home flow.
- **D-02:** Above-the-fold hierarchy should be: date-range controls, KPI summary tiles (total/positive/negative), then charts.
- **D-03:** Keep current visual language (glass panels, gradient atmosphere, Tailwind utility patterns) for consistency with existing pages.

### Charting and Presentation
- **D-04:** Use Chart.js in Phase 3 as the lightweight chart stack aligned with project constraints.
- **D-05:** Sentiment distribution should use a compact doughnut chart plus explicit count/percentage labels in adjacent KPI cards.
- **D-06:** Sentiment trend should use a multi-series line chart (positive vs negative over day buckets) with clear legend and tooltip values.

### Date Range UX
- **D-07:** Default dashboard range is last 30 days on first load.
- **D-08:** Provide quick presets: 7 days, 30 days, 90 days, all time.
- **D-09:** Include custom start/end date inputs with explicit `Apply` action to avoid accidental repeated refreshes.

### Data Scope and API Surface
- **D-10:** Phase 3 dashboard aggregates all persisted events (single/api/batch combined); source-level segmentation is deferred.
- **D-11:** Add dedicated dashboard data endpoints for distribution and trend payloads rather than embedding chart JSON in templates.
- **D-12:** Empty-state messaging must be explicit when no events exist for selected range and should guide users back to prediction/batch flows.

### Agent's Discretion
- Exact color palette mapping per sentiment series as long as contrast/readability remains high.
- Whether dashboard endpoints are split (`/api/dashboard/distribution` and `/api/dashboard/trend`) or consolidated (`/api/dashboard/summary`) if response contracts remain clear.
- Minor animation choices for chart entrance and KPI transitions.

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Scope and requirements
- `.planning/ROADMAP.md` - Phase 3 goal, dependencies, and success criteria.
- `.planning/REQUIREMENTS.md` - DASH-01, DASH-02, DASH-03 requirements contract.
- `.planning/PROJECT.md` - architecture constraints and stakeholder-focused product framing.

### Upstream phase outputs
- `.planning/phases/01-analytics-data-foundation/01-VERIFICATION.md` - validated persistence substrate and analytics primitives.
- `.planning/phases/02-batch-csv-analysis-pipeline/02-VERIFICATION.md` - validated batch pipeline and event expansion.
- `.planning/phases/02-batch-csv-analysis-pipeline/02-CONTEXT.md` - prior dashboard-relevant decisions around clarity and reporting style.

### Code integration anchors
- `app.py` - current route architecture and response patterns.
- `storage/history_store.py` - `count_by_sentiment` and `trend_by_day` primitives used for dashboard data.
- `templates/base.html` - shared layout shell where dashboard navigation/linking should remain consistent.
- `static/css/app.css` - current visual language and reusable panel/motion styling.
- `static/js/app.js` - current client-side pattern for lightweight page interactions.

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- `HistoryStore.count_by_sentiment(start_ts, end_ts)` already supports range-bounded distribution aggregations.
- `HistoryStore.trend_by_day(start_ts, end_ts)` already emits day-bucket trend rows suitable for chart series transformation.
- Existing `base_context` pattern in `app.py` provides a stable mechanism for passing page-level metadata.

### Established Patterns
- Flask monolith with Jinja-rendered pages and optional JSON endpoints.
- Tailwind + custom CSS design system with glass cards and animated reveal patterns.
- Lightweight vanilla JS enhancements, no SPA framework.

### Integration Points
- Add dashboard page route(s) in `app.py` and reuse existing app-wide context metadata.
- Add dashboard data API endpoints in `app.py` that call `HistoryStore` aggregations with date filters.
- Add new dashboard template (for example `templates/dashboard.html`) and dashboard-specific JS file or module to mount Chart.js instances.

</code_context>

<specifics>
## Specific Ideas

- KPI strip should explicitly show both raw counts and percentages to satisfy stakeholder clarity quickly.
- Trend chart tooltips should include date + count per series for presentation walkthroughs.
- Empty range state should include actionable guidance: "Try broader date range" and link to prediction/batch pages.

</specifics>

<deferred>
## Deferred Ideas

- Source-segment drilldowns (`single` vs `api` vs `batch`) and interactive toggles.
- Comparative multi-metric dashboard cards beyond sentiment distribution/trend.
- Real-time auto-refresh and websocket-driven updates.

These remain out of Phase 3 scope.

</deferred>

---

*Phase: 03-dashboard-visualization-layer*
*Context gathered: 2026-04-02*
