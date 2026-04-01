# Phase 3: Dashboard Visualization Layer - Research

**Researched:** 2026-04-02
**Domain:** Flask dashboard visualization (Chart.js + SQLite-backed analytics)
**Confidence:** HIGH

<user_constraints>
## User Constraints (from CONTEXT.md)

### Locked Decisions
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

### Claude's Discretion
- Exact color palette mapping per sentiment series as long as contrast/readability remains high.
- Whether dashboard endpoints are split (`/api/dashboard/distribution` and `/api/dashboard/trend`) or consolidated (`/api/dashboard/summary`) if response contracts remain clear.
- Minor animation choices for chart entrance and KPI transitions.

### Deferred Ideas (OUT OF SCOPE)
- Source-segment drilldowns (`single` vs `api` vs `batch`) and interactive toggles.
- Comparative multi-metric dashboard cards beyond sentiment distribution/trend.
- Real-time auto-refresh and websocket-driven updates.

These remain out of Phase 3 scope.
</user_constraints>

<phase_requirements>
## Phase Requirements

| ID | Description | Research Support |
|----|-------------|------------------|
| DASH-01 | User can view sentiment distribution counts and percentages for analyzed reviews. | Use `HistoryStore.count_by_sentiment` + backend percentage calculation + doughnut chart + KPI tiles. |
| DASH-02 | User can view sentiment trend over time using timestamped review data. | Use `HistoryStore.trend_by_day`, normalize sparse rows into dense day-label series, render multi-series line chart. |
| DASH-03 | User can filter dashboard trend data by selectable date range. | Use date presets + custom start/end inputs + backend UTC range normalization + query-param driven data endpoints. |
</phase_requirements>

## Summary

Phase 3 should be implemented as a server-rendered dashboard shell (`/dashboard`) plus JSON data endpoints for chart payloads. The codebase already has the key analytics primitives in `storage/history_store.py` (`count_by_sentiment`, `trend_by_day`), so the work is primarily response shaping, range filtering, and frontend chart state management.

The most important technical decision is to use Chart.js line + doughnut with a category X-axis (`YYYY-MM-DD` labels) instead of a time scale for v1. This avoids adapter complexity while satisfying DASH-02 and DASH-03. If you switch to Chart.js time scale later, official docs require a date adapter and date library.

Date filtering must be normalized in the backend. Current storage compares ISO timestamp strings (`created_at`) and can silently exclude same-day rows if end dates are passed as plain `YYYY-MM-DD`. Plan explicit range conversion (inclusive start, inclusive end-day via next-day-exclusive or `23:59:59.999999`) and test these edges first.

**Primary recommendation:** Build `/dashboard` + split endpoints (`/api/dashboard/distribution`, `/api/dashboard/trend`) and keep trend chart on category labels with backend-normalized UTC date ranges.

## Project Constraints (from CLAUDE.md)

- Keep Flask backend architecture; do not introduce SPA/frontend framework expansion.
- Use a lightweight JavaScript chart stack (Chart.js is aligned and explicitly chosen).
- Preserve v1 scope boundaries (dashboard/trend/filter only for this phase; no auth, no advanced segmentation).
- Optimize for internal/demo stakeholder clarity and presentability (explicit metrics, understandable visuals).
- Maintain compatibility with existing pickle-based inference pipeline and current app runtime assumptions.
- Follow existing monolithic conventions: implement in root `app.py`, root `templates/`, and root `static/` (not nested duplicate project copy).
- Keep existing dual-surface pattern (HTML view + JSON endpoints) and explicit error handling semantics.
- Continue snake_case Python naming and helper-based validation patterns.

## Standard Stack

### Core
| Library | Version | Purpose | Why Standard |
|---------|---------|---------|--------------|
| Flask | Repo pin `2.1.2` (`requirements.txt`), local runtime observed `3.0.0` | Route + template + JSON endpoint layer | Existing app is Flask monolith; Phase 3 should extend existing route patterns, not replatform. |
| Chart.js | `4.5.1` (npm latest, published 2025-10-13 UTC) | Doughnut + line chart rendering | Officially supports both chart types needed and works with plain script-tag integration. |
| SQLite (`sqlite3`) | 3.35.5 (local runtime) | Persisted analytics source queried via `HistoryStore` | Existing persisted history is already in SQLite; no new datastore needed. |

### Supporting
| Library | Version | Purpose | When to Use |
|---------|---------|---------|-------------|
| chartjs-adapter-date-fns | `3.0.0` (latest, published 2022-12-11 UTC) | Date adapter for Chart.js time scale | Only if you choose `type: "time"` axis in future; not required for category labels. |
| pytest | 8.4.0 (local runtime) | Automated verification of route/data/filter behavior | Required for Nyquist validation and phase gate checks. |

### Alternatives Considered
| Instead of | Could Use | Tradeoff |
|------------|-----------|----------|
| Category X-axis (`YYYY-MM-DD` labels) | Chart.js time axis + adapter | Time axis gives richer scale behavior, but adds adapter/date-lib complexity and extra failure modes. |
| Split dashboard endpoints | Single `/api/dashboard/summary` endpoint | Single endpoint reduces requests, but split endpoints simplify payload contracts and isolated testing. |
| Chart.js | Hand-rolled SVG/canvas | Custom charts are slower to build/test and introduce avoidable rendering edge cases. |

**Installation:**
```bash
# If you choose package-managed frontend assets
npm install chart.js

# Optional only for time-scale axis (not needed for category labels)
npm install chartjs-adapter-date-fns date-fns
```

**Version verification:** Verified via registry on 2026-04-02.
- `npm view chart.js version` -> `4.5.1`
- `npm view chart.js time` -> `4.5.1` published `2025-10-13T08:54:35.850Z`
- `npm view chartjs-adapter-date-fns version` -> `3.0.0`
- `npm view chartjs-adapter-date-fns time` -> `3.0.0` published `2022-12-11T00:10:19.186Z`

## Architecture Patterns

### Recommended Project Structure
```
app.py                          # Add dashboard page route + dashboard API endpoints
templates/
  dashboard.html                # Dashboard shell: filters, KPI cards, chart canvases, empty states
static/js/
  dashboard.js                  # Fetch endpoints, transform payloads, own Chart instances
tests/
  test_dashboard_endpoints.py   # API payload and filtering assertions
  test_dashboard_ui_integration.py  # Dashboard page render + empty-state assertions
```

### Pattern 1: Server-Rendered Shell + JSON Data Endpoints
**What:** Render `/dashboard` HTML skeleton server-side; fetch chart payloads from dedicated `/api/dashboard/*` endpoints.
**When to use:** Flask monolith with existing Jinja templates and lightweight JS enhancement.
**Example:**
```python
# Source: https://flask.palletsprojects.com/en/stable/quickstart/
# request.args.get(...) for query params, jsonify(...) for JSON payload
@app.get("/api/dashboard/distribution")
def dashboard_distribution():
    range_key = request.args.get("range", "30d")
    start_ts, end_ts = resolve_range(range_key, request.args.get("start"), request.args.get("end"))
    counts = history_store.count_by_sentiment(start_ts, end_ts)
    return jsonify(build_distribution_payload(counts))
```

### Pattern 2: Backend Date-Range Normalization Before Querying
**What:** Convert user date input (`YYYY-MM-DD`) into explicit UTC boundaries before SQL filtering.
**When to use:** Anytime filters come from date pickers and stored timestamps include time zone/time components.
**Example:**
```python
# Source: https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/input/date
# Source: https://www.sqlite.org/lang_datefunc.html
def normalize_date_bounds(start_date: str | None, end_date: str | None):
    # Inputs are yyyy-mm-dd from <input type="date">
    # Use [start, next_day(end)) to keep end-date inclusive for full day
    ...
```

### Pattern 3: Persistent Chart Instances + Incremental Updates
**What:** Create chart instances once, then update `data.labels`, `data.datasets`, call `chart.update()` (or `update("none")`).
**When to use:** Re-filtering dashboard charts repeatedly via presets/custom date apply.
**Example:**
```javascript
// Source: https://www.chartjs.org/docs/latest/developers/updates.html
distributionChart.data.labels = payload.labels;
distributionChart.data.datasets[0].data = payload.counts;
distributionChart.update("none");
```

### Anti-Patterns to Avoid
- **Building chart data in Jinja context only:** Harder to test filter behavior and contracts; use explicit JSON endpoints.
- **Using Chart.js `time` scale without adapter setup:** Official docs require date library + adapter; avoid unless deliberately configured.
- **Recreating charts on each filter click:** Causes stale instances and inconsistent UI state; update existing instances instead.
- **Passing raw `YYYY-MM-DD` directly as `end_ts` to current SQL comparisons:** Can exclude same-day events due lexical timestamp comparison.

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| Chart rendering | Custom canvas/SVG drawing engine | Chart.js doughnut + line charts | Built-in interactions, legends, tooltips, responsive behavior. |
| Date-picker widgets | Custom calendar UI | Native `<input type="date">` + preset buttons | Browser-normalized value format and less UI maintenance. |
| Query parsing | Manual URL string parsing | Flask `request.args.get(...)` + explicit range resolver | Safer parsing and clearer endpoint contracts. |
| Trend bucket math in JS-only | Client-side ad-hoc grouping from raw events | `HistoryStore.trend_by_day` + server payload shaping | Reuses persistence layer primitives and keeps logic testable server-side. |

**Key insight:** The backend already has aggregation primitives; Phase 3 should standardize contracts and visualization behavior, not introduce new custom analytics engines.

## Common Pitfalls

### Pitfall 1: End-Date Exclusion Bug
**What goes wrong:** Records on selected end date are missing from distribution/trend.
**Why it happens:** Stored `created_at` includes time (`2026-04-01T...`) but filter is plain `YYYY-MM-DD`; string comparison with `<= end_date` drops same-day timestamps.
**How to avoid:** Normalize to UTC timestamp range and use inclusive-day semantics (`start <= ts < next_day(end)`).
**Warning signs:** Dashboard counts are lower than expected when filtering a single day.

### Pitfall 2: Sparse Trend Series Misalignment
**What goes wrong:** Positive and negative lines shift or have unequal lengths.
**Why it happens:** `trend_by_day` returns only existing `(day, label)` rows, not zero-filled missing combinations.
**How to avoid:** Build a complete day label sequence and backfill missing label/day cells with `0`.
**Warning signs:** Tooltip dates mismatch between series; jagged gaps with missing points.

### Pitfall 3: Chart Instance Leaks During Refilter
**What goes wrong:** Multiple charts render on top of each other or memory grows after repeated filtering.
**Why it happens:** New `Chart(...)` created per update without reusing/destroying instance.
**How to avoid:** Keep one instance per canvas, mutate data/options, then call `update()`.
**Warning signs:** Duplicate legend entries, delayed UI response after many filter changes.

### Pitfall 4: Time-Scale Adapter Trap
**What goes wrong:** Time-axis chart fails or mis-parses dates.
**Why it happens:** Chart.js time scale requires external date adapter/date library.
**How to avoid:** Use category axis for v1 day buckets; if switching to time axis, install and load adapter deliberately.
**Warning signs:** Console errors around adapter/time parsing and empty chart render.

## Code Examples

Verified patterns from official sources and current project architecture:

### Dashboard Endpoint Query Parsing
```python
# Source: https://flask.palletsprojects.com/en/stable/quickstart/
@app.get("/api/dashboard/trend")
def dashboard_trend():
    preset = request.args.get("range", "30d")
    start = request.args.get("start")
    end = request.args.get("end")
    start_ts, end_ts = resolve_range(preset, start, end)
    rows = history_store.trend_by_day(start_ts, end_ts)
    return jsonify(build_trend_payload(rows))
```

### Category-Axis Line Chart for Day Buckets
```javascript
// Source: https://www.chartjs.org/docs/latest/axes/cartesian/category.html
const trendChart = new Chart(ctx, {
  type: "line",
  data: {
    labels: payload.labels, // ["2026-04-01", "2026-04-02", ...]
    datasets: [
      { label: "Positive", data: payload.series.positive },
      { label: "Negative", data: payload.series.negative }
    ]
  }
});
```

### Doughnut Chart Data Contract
```javascript
// Source: https://www.chartjs.org/docs/latest/charts/doughnut.html
const distributionChart = new Chart(ctx, {
  type: "doughnut",
  data: {
    labels: ["Positive", "Negative"],
    datasets: [{ data: [payload.positive.count, payload.negative.count] }]
  }
});
```

### Tooltip Label Formatting
```javascript
// Source: https://www.chartjs.org/docs/latest/configuration/tooltip.html
options: {
  plugins: {
    tooltip: {
      callbacks: {
        label(context) {
          return `${context.dataset.label}: ${context.parsed.y}`;
        }
      }
    }
  }
}
```

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|--------|
| Static page with single-review result only | Data-driven dashboard with split API endpoints + client chart rendering | Current phase target (2026) | Enables stakeholder trend narrative and filterable analytics. |
| Time axis by default assumption | Category axis for `YYYY-MM-DD` day buckets in v1 | Recommended for this phase | Avoids date-adapter complexity while meeting DASH-02/03. |
| Full chart re-instantiation per refresh | Mutate data + `chart.update()` | Chart.js documented current pattern (updated docs 2025-10-13) | Lower UI churn, fewer memory/state bugs. |

**Deprecated/outdated:**
- Building visualization payloads only in template context for dynamic filters: replaced by dedicated JSON endpoints.
- Assuming raw string date bounds are sufficient for timestamped storage: must normalize date range semantics.

## Open Questions

1. **Endpoint shape finalization (split vs consolidated)**
   - What we know: Both are allowed by discretion; split endpoints improve isolated testing and contract clarity.
   - What's unclear: Whether future Phase 4 metrics should be fetched in same call for performance.
   - Recommendation: Use split endpoints now; revisit consolidation when metrics panel lands.

2. **Timezone semantics for custom date filters**
   - What we know: Stored timestamps are UTC; browser date inputs are locale-driven but submit `YYYY-MM-DD`.
   - What's unclear: Whether stakeholders expect local-day or UTC-day buckets.
   - Recommendation: Define UTC in v1 UI helper text and keep backend/filter/tests UTC-consistent.

## Environment Availability

| Dependency | Required By | Available | Version | Fallback |
|------------|------------|-----------|---------|----------|
| Python | Flask app + tests | Yes | 3.10.0 | - |
| Flask runtime | Dashboard routes/endpoints | Yes | 3.0.0 installed (repo pin is 2.1.2) | Align env to `requirements.txt` if reproducibility issues appear |
| SQLite (`sqlite3`) | History aggregations | Yes | 3.35.5 | - |
| pytest | Nyquist validation | Yes | 8.4.0 | - |
| Node/npm | Optional local Chart.js vendoring | Yes | Node 22.16.0 / npm 11.12.0 | Use CDN script tag without npm |
| Chart.js local package | Frontend charts | No (not installed in repo) | - | Load via CDN (`chart.umd.min.js`) or vendor static file |

**Missing dependencies with no fallback:**
- None.

**Missing dependencies with fallback:**
- Local Chart.js package install (fallback: CDN script or checked-in static vendor file).

## Validation Architecture

### Test Framework
| Property | Value |
|----------|-------|
| Framework | pytest 8.4.0 |
| Config file | none - tests run via defaults |
| Quick run command | `python -m pytest tests/test_dashboard_endpoints.py -q` |
| Full suite command | `python -m pytest -q` |

### Phase Requirements -> Test Map
| Req ID | Behavior | Test Type | Automated Command | File Exists? |
|--------|----------|-----------|-------------------|-------------|
| DASH-01 | Distribution endpoint returns counts + percentages and dashboard shows KPI totals | integration | `python -m pytest tests/test_dashboard_endpoints.py::test_distribution_payload_counts_and_percentages -q` | No Wave 0 |
| DASH-02 | Trend endpoint returns day-bucket positive/negative series aligned for line chart | integration + unit transform | `python -m pytest tests/test_dashboard_endpoints.py::test_trend_payload_has_aligned_series -q` | No Wave 0 |
| DASH-03 | Preset/custom date ranges filter distribution/trend correctly, including edge-day inclusivity | integration | `python -m pytest tests/test_dashboard_endpoints.py::test_date_range_filters_are_inclusive -q` | No Wave 0 |

### Sampling Rate
- **Per task commit:** `python -m pytest tests/test_dashboard_endpoints.py -q`
- **Per wave merge:** `python -m pytest -q`
- **Phase gate:** Full suite green before `/gsd:verify-work`

### Wave 0 Gaps
- [ ] `tests/test_dashboard_endpoints.py` - API contract + date-range behavior for DASH-01/02/03
- [ ] `tests/test_dashboard_page.py` - `/dashboard` render + empty-state assertions
- [ ] `static/js/dashboard.js` behavior verification strategy (manual smoke checklist or lightweight JS test harness)

## Sources

### Primary (HIGH confidence)
- Local codebase:
  - `app.py` - current Flask route, JSON endpoint, and context patterns
  - `storage/history_store.py` - existing `count_by_sentiment` and `trend_by_day` primitives
  - `templates/base.html`, `static/js/app.js`, `tests/*.py` - UI/JS/test conventions
- Chart.js official docs:
  - https://www.chartjs.org/docs/latest/getting-started/installation.html
  - https://www.chartjs.org/docs/latest/getting-started/integration.html
  - https://www.chartjs.org/docs/latest/charts/doughnut.html
  - https://www.chartjs.org/docs/latest/charts/line.html
  - https://www.chartjs.org/docs/latest/axes/cartesian/category.html
  - https://www.chartjs.org/docs/latest/axes/cartesian/time.html
  - https://www.chartjs.org/docs/latest/developers/updates.html
  - https://www.chartjs.org/docs/latest/configuration/tooltip.html
- Flask official docs:
  - https://flask.palletsprojects.com/en/stable/quickstart/
  - https://flask.palletsprojects.com/en/stable/api/
  - https://flask.palletsprojects.com/en/stable/testing/
- SQLite official docs:
  - https://www.sqlite.org/lang_datefunc.html
- MDN official docs:
  - https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/input/date
- Registry verification (run locally on 2026-04-02):
  - `npm view chart.js version`
  - `npm view chart.js time`
  - `npm view chartjs-adapter-date-fns version`
  - `npm view chartjs-adapter-date-fns time`

### Secondary (MEDIUM confidence)
- None.

### Tertiary (LOW confidence)
- None.

## Metadata

**Confidence breakdown:**
- Standard stack: HIGH - direct official docs + registry verification + existing code constraints.
- Architecture: HIGH - aligned with locked decisions and existing Flask/Jinja project structure.
- Pitfalls: MEDIUM-HIGH - strongly supported by current storage/query patterns and official date/Chart.js docs; timezone expectation still requires product call.

**Research date:** 2026-04-02
**Valid until:** 2026-05-02 (30 days; revisit if Chart.js/Flask stack decisions change)
