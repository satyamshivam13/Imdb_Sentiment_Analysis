# Feature Research

**Domain:** Sentiment analytics web application
**Researched:** 2026-04-02
**Confidence:** HIGH

## Feature Landscape

### Table Stakes (Users Expect These)

| Feature | Why Expected | Complexity | Notes |
|---------|--------------|------------|-------|
| Single review prediction | Baseline sentiment app behavior | LOW | Already validated in current app |
| Basic confidence display | Stakeholders need trust context | LOW | Already present; can expand with metric explanations |
| Health/readiness endpoint | Demo reliability and ops confidence | LOW | Already available as `/health` |

### Differentiators (Competitive Advantage)

| Feature | Value Proposition | Complexity | Notes |
|---------|-------------------|------------|-------|
| Analytics dashboard | Moves app from toy predictor to insight tool | MEDIUM | Chart layer + aggregation pipeline |
| Batch CSV analysis | Enables practical workflow beyond manual entry | MEDIUM | Needs validation and export path |
| Model metrics panel | Improves transparency for stakeholder demos | MEDIUM | Use precomputed metrics and confusion matrix |
| Review history and trends | Shows temporal narrative, not isolated outputs | MEDIUM | Requires persistence and date grouping |

### Anti-Features (Commonly Requested, Often Problematic)

| Feature | Why Requested | Why Problematic | Alternative |
|---------|---------------|-----------------|-------------|
| Full user auth in v1 | Feels productized | High implementation overhead for low immediate value | Defer to v2 |
| Multi-model benchmarking in v1 | Looks advanced | Can dilute delivery focus before baseline analytics is stable | Add after v1 analytics is complete |

## Feature Dependencies

```text
Batch CSV analysis
    -> requires -> CSV validation + parsing
    -> requires -> aggregation service

Analytics dashboard
    -> requires -> aggregated sentiment data

Review history trends
    -> requires -> persistence layer
    -> enhances -> dashboard trend visuals

Model metrics panel
    -> requires -> metric generation artifact
```

## MVP Definition

### Launch With (v1)

- [ ] Dashboard distribution and trend charts
- [ ] Model metrics and confusion matrix display
- [ ] Batch CSV ingestion and export
- [ ] Review history with trend filtering (no auth)

### Add After Validation (v1.x)

- [ ] API documentation explorer
- [ ] Improved metric slicing by source/time window

### Future Consideration (v2+)

- [ ] Authentication and per-user saved analytics
- [ ] Multi-model A/B comparison workflows
- [ ] PWA/mobile packaging

## Feature Prioritization Matrix

| Feature | User Value | Implementation Cost | Priority |
|---------|------------|---------------------|----------|
| Dashboard charts | HIGH | MEDIUM | P1 |
| Metrics panel | HIGH | MEDIUM | P1 |
| Batch CSV analysis | HIGH | MEDIUM | P1 |
| Review history trends | HIGH | MEDIUM | P1 |
| API docs explorer | MEDIUM | MEDIUM | P2 |
| Auth system | MEDIUM | HIGH | P3 |

---
*Feature research for: sentiment analytics web application*
*Researched: 2026-04-02*
