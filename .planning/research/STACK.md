# Stack Research

**Domain:** Sentiment analytics web application
**Researched:** 2026-04-02
**Confidence:** HIGH

## Recommended Stack

### Core Technologies

| Technology | Version | Purpose | Why Recommended |
|------------|---------|---------|-----------------|
| Flask | 2.x | API + server-rendered pages | Matches current codebase and deployment path |
| scikit-learn | 1.x | Sentiment inference + metrics utilities | Already used by model pipeline and supports eval metrics cleanly |
| Chart.js | 4.x | Sentiment distribution and trend visualization | Lightweight integration for non-SPA dashboards |
| pandas | 1.x+ | CSV ingestion and batch transformation | Reliable for batch review analysis and export workflows |

### Supporting Libraries

| Library | Version | Purpose | When to Use |
|---------|---------|---------|-------------|
| numpy | 1.x | Numeric support for metrics and arrays | Required by scikit-learn stack |
| Flask-WTF or manual validation | latest compatible | Input/upload validation | Use when CSV upload validations grow |
| python-dateutil | latest compatible | Timeline normalization | Use for robust date grouping in trend charts |

### Development Tools

| Tool | Purpose | Notes |
|------|---------|-------|
| pytest | Automated testing | Add endpoint and CSV parser tests early |
| gunicorn | Production serving | Already used via `Procfile` |

## Alternatives Considered

| Recommended | Alternative | When to Use Alternative |
|-------------|-------------|-------------------------|
| Flask + templates | React/Vue SPA | If product later needs highly interactive multi-user dashboards |
| Chart.js | Plotly | If advanced drill-down analytics become a primary feature |
| Local pickle artifacts | Model serving microservice | If frequent model swaps or online retraining is needed |

## What NOT to Use

| Avoid | Why | Use Instead |
|-------|-----|-------------|
| Full SPA rewrite in v1 | Increases scope and delivery risk | Keep Flask + lightweight JS charts |
| Auth-first implementation | Distracts from core analytics value | Defer auth to v2 as decided |

## Stack Patterns by Variant

**If stakeholder demos remain primary use case:**
- Use server-rendered dashboard + incremental JS enhancements
- Because it keeps iteration speed high and complexity low

**If external API consumers become primary:**
- Add stronger API contracts and docs layer
- Because integration reliability matters more than UI polish

## Sources

- Existing repository stack and deployment artifacts
- Current requirements and stakeholder focus in `.planning/PROJECT.md`
- Common sentiment analytics implementation patterns

---
*Stack research for: sentiment analytics web application*
*Researched: 2026-04-02*
