# Pitfalls Research

**Domain:** Sentiment analytics web application
**Researched:** 2026-04-02
**Confidence:** HIGH

## Critical Pitfalls

### Pitfall 1: Dashboard without trustworthy data lineage

**What goes wrong:** Charts look polished but stakeholders cannot trust where numbers came from.
**Why it happens:** Aggregation logic is added quickly without provenance fields.
**How to avoid:** Record timestamps, source type, and aggregation definitions in one service layer.
**Warning signs:** Same dataset gives inconsistent chart totals across pages.
**Phase to address:** Phase 1 and Phase 2.

---

### Pitfall 2: CSV batch ingestion silently accepting bad schema

**What goes wrong:** Mixed columns or empty rows produce incorrect sentiment totals.
**Why it happens:** Weak upload validation and implicit column guessing.
**How to avoid:** Enforce required review column, reject malformed rows, return detailed validation errors.
**Warning signs:** Export row counts do not match upload row counts.
**Phase to address:** Phase 2.

---

### Pitfall 3: Metric panel showing stale or mismatched model stats

**What goes wrong:** Accuracy/F1 displayed does not correspond to current loaded model artifact.
**Why it happens:** Metrics are hardcoded or not version-linked to model files.
**How to avoid:** Persist model metadata and metric artifact versions together.
**Warning signs:** Model file changes but metrics panel remains identical.
**Phase to address:** Phase 3 and Phase 4.

---

### Pitfall 4: History storage growth and performance degradation

**What goes wrong:** Trend views become slow as historical rows increase.
**Why it happens:** Full history scans for every dashboard request.
**How to avoid:** Add indexed timestamp queries and summary caches for trend windows.
**Warning signs:** Dashboard load time grows linearly with history size.
**Phase to address:** Phase 1 and Phase 5.

## Technical Debt Patterns

| Shortcut | Immediate Benefit | Long-term Cost | When Acceptable |
|----------|-------------------|----------------|-----------------|
| Keep all analytics logic in `app.py` | Faster initial coding | Hard-to-test monolith and regression risk | Only temporarily during migration |
| Manual CSV parsing in routes | Quick prototype | Fragile edge-case behavior | Never for v1 release |
| Hardcoded metrics in template | Fast UI mockup | Loss of model trustworthiness | Demo-only throwaway branch |

## Security Mistakes

| Mistake | Risk | Prevention |
|---------|------|------------|
| Unbounded CSV upload size | Memory pressure and denial risk | Set size limits and row caps |
| Persisting raw review content without governance | Sensitive text exposure in logs/storage | Sanitize logs and define retention policy |
| Blind trust of pickle artifacts | Code execution risk from tampered files | Restrict artifact writes and validate provenance |

## "Looks Done But Isn't" Checklist

- [ ] Dashboard totals match batch output aggregates
- [ ] CSV parser handles empty, malformed, and oversized files
- [ ] Metrics panel is tied to identifiable model version
- [ ] History trend filters are validated and timezone-safe

## Pitfall-to-Phase Mapping

| Pitfall | Prevention Phase | Verification |
|---------|------------------|--------------|
| Data lineage mismatch | Phase 1 | Aggregation tests and trace fields present |
| CSV schema drift | Phase 2 | Upload validation tests and row parity checks |
| Stale metrics | Phase 4 | Metric artifact version check in UI |
| Slow trend rendering | Phase 5 | Baseline perf checks on history queries |

---
*Pitfalls research for: sentiment analytics web application*
*Researched: 2026-04-02*
