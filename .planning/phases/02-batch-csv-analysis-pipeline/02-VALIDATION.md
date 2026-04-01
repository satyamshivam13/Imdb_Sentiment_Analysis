---
phase: 02
slug: batch-csv-analysis-pipeline
status: ready
nyquist_compliant: true
wave_0_complete: true
created: 2026-04-02
updated: 2026-04-02
---

# Phase 02 - Validation Strategy

> Per-phase validation contract for feedback sampling during execution.

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | pytest |
| **Config file** | none - existing pytest execution via `python -m pytest` |
| **Quick run command** | `python -m pytest tests/test_batch_service.py -q` |
| **Full suite command** | `python -m pytest -q` |
| **Estimated runtime** | ~45 seconds |

---

## Sampling Rate

- **After every task commit:** Run `python -m pytest tests/test_batch_service.py -q` when batch tests exist
- **After every plan wave:** Run `python -m pytest -q`
- **Before `$gsd-verify-work`:** Full suite must be green
- **Max feedback latency:** 90 seconds

---

## Per-Task Verification Map

| Task ID | Plan | Wave | Requirement | Test Type | Automated Command | File Exists | Status |
|---------|------|------|-------------|-----------|-------------------|-------------|--------|
| 02-01-01 | 01 | 1 | BATCH-01,BATCH-02 | unit | `python -m pytest tests/test_csv_validation.py -q` | yes | green |
| 02-02-01 | 02 | 2 | BATCH-03 | service | `python -m pytest tests/test_batch_service.py -q` | yes | green |
| 02-03-01 | 03 | 3 | BATCH-04,BATCH-05 | integration | `python -m pytest tests/test_batch_integration.py -q` | yes | green |

---

## Wave 0 Requirements

- [x] `tests/test_csv_validation.py` - schema and row validation coverage
- [x] `tests/test_batch_service.py` - scoring + metrics + persistence behavior
- [x] `tests/test_batch_integration.py` - endpoint upload/export integration checks

---

## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions |
|----------|-------------|------------|-------------------|
| Stakeholder-friendly batch results UX (upload feedback and download discoverability) | BATCH-01,BATCH-04,BATCH-05 | Visual clarity and messaging quality are subjective | Run app, upload valid and mixed CSV files, confirm error blocks and download affordance are understandable |

---

## Validation Sign-Off

- [x] All tasks have automated verify or explicit Wave 0 dependencies
- [x] Sampling continuity preserved
- [x] No watch-mode flags
- [x] Feedback latency < 90s
- [x] `nyquist_compliant: true` set in frontmatter after execution verification

**Approval:** approved 2026-04-02
