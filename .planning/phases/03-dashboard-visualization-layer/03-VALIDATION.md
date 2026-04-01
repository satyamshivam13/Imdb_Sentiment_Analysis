---
phase: 3
slug: dashboard-visualization-layer
status: draft
nyquist_compliant: false
wave_0_complete: false
created: 2026-04-02
---

# Phase 3 - Validation Strategy

> Per-phase validation contract for feedback sampling during execution.

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | pytest 8.4.0 |
| **Config file** | none (pytest defaults) |
| **Quick run command** | `python -m pytest tests/test_dashboard_endpoints.py -q` |
| **Full suite command** | `python -m pytest -q` |
| **Estimated runtime** | ~30-90 seconds |

---

## Sampling Rate

- **After every task commit:** Run `python -m pytest tests/test_dashboard_endpoints.py -q`
- **After every plan wave:** Run `python -m pytest -q`
- **Before `$gsd-verify-work`:** Full suite must be green
- **Max feedback latency:** 90 seconds

---

## Per-Task Verification Map

| Task ID | Plan | Wave | Requirement | Test Type | Automated Command | File Exists | Status |
|---------|------|------|-------------|-----------|-------------------|-------------|--------|
| 03-01-01 | 01 | 1 | DASH-01 | integration | `python -m pytest tests/test_dashboard_endpoints.py::test_distribution_payload_counts_and_percentages -q` | ❌ W0 | ⬜ pending |
| 03-02-01 | 02 | 2 | DASH-02 | integration | `python -m pytest tests/test_dashboard_endpoints.py::test_trend_payload_has_aligned_series -q` | ❌ W0 | ⬜ pending |
| 03-03-01 | 03 | 2 | DASH-03 | integration | `python -m pytest tests/test_dashboard_endpoints.py::test_date_range_filters_are_inclusive -q` | ❌ W0 | ⬜ pending |

*Status: ⬜ pending · ✅ green · ❌ red · ⚠️ flaky*

---

## Wave 0 Requirements

- [ ] `tests/test_dashboard_endpoints.py` - API contract and date-range behavior for DASH-01/DASH-02/DASH-03
- [ ] `tests/test_dashboard_page.py` - `/dashboard` render and empty-state assertions
- [ ] Dashboard JS verification strategy documented (manual smoke checklist or automated harness)

---

## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions |
|----------|-------------|------------|-------------------|
| Chart tooltip readability and legend clarity | DASH-01, DASH-02 | Visual UX behavior is not fully asserted by backend tests | Open `/dashboard`, switch presets (7/30/90/all), confirm doughnut + line legends/tooltip labels map to expected counts |
| Empty-state guidance quality | DASH-03 | Messaging usefulness is content/UX quality focused | Filter into date range with no events and verify guidance text appears with navigation cues to predict/batch flows |

---

## Validation Sign-Off

- [ ] All tasks have `<automated>` verify or Wave 0 dependencies
- [ ] Sampling continuity: no 3 consecutive tasks without automated verify
- [ ] Wave 0 covers all MISSING references
- [ ] No watch-mode flags
- [ ] Feedback latency < 90s
- [ ] `nyquist_compliant: true` set in frontmatter

**Approval:** pending
