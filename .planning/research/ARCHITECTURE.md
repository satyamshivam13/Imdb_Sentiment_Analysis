# Architecture Research

**Domain:** Sentiment analytics web application
**Researched:** 2026-04-02
**Confidence:** HIGH

## Standard Architecture

### System Overview

```text
Client (browser)
    -> Flask routes (HTML + JSON)
        -> Validation layer
            -> Inference service (model + vectorizer)
            -> Analytics service (aggregation, metrics)
            -> Batch service (CSV parse, per-row scoring, export)
                -> Persistence (history store)
```

### Component Responsibilities

| Component | Responsibility | Typical Implementation |
|-----------|----------------|------------------------|
| Route handlers | Input/output contracts | Flask routes in `app.py` or `routes/` modules |
| Inference service | Single text scoring | Wrapper around vectorizer + model predict APIs |
| Batch service | Multi-row processing and exports | pandas pipeline with strict column validation |
| Analytics service | Distribution and trend aggregation | Grouping by label and timestamp buckets |
| Metrics service | Evaluation artifact loading/rendering | JSON or CSV metric files generated offline |
| History store | Persist analyzed review records | SQLite/file-backed store for v1 |

## Recommended Project Structure

```text
app.py
services/
  inference.py
  batch.py
  analytics.py
  metrics.py
storage/
  history.py
templates/
static/
tests/
```

## Architectural Patterns

### Pattern 1: Service Extraction from Monolith

**What:** Move logic from route handlers into focused service modules.
**When to use:** As soon as batch + dashboard logic enters the app.
**Trade-offs:** Small initial refactor cost, major long-term maintainability gain.

### Pattern 2: Precompute Then Render Metrics

**What:** Compute model performance artifacts once and render fast.
**When to use:** Dashboard metrics panels where reproducibility matters.
**Trade-offs:** Requires refresh workflow, avoids expensive runtime recomputation.

### Pattern 3: Pipeline-Oriented Batch Processing

**What:** Validate -> transform -> score -> aggregate -> export.
**When to use:** CSV upload and report generation flows.
**Trade-offs:** Slightly more code structure, much safer error handling.

## Data Flow

1. User uploads reviews or submits individual review.
2. Validation normalizes payload and rejects malformed input.
3. Inference service returns label + confidence.
4. History store records result events.
5. Analytics service computes dashboard aggregates.
6. Templates/charts render insights for stakeholder consumption.

## Scaling Considerations

| Scale | Architecture Adjustments |
|-------|--------------------------|
| 0-1k demo sessions | Flask monolith is sufficient |
| 1k-50k sessions | Add caching for expensive aggregates |
| 50k+ sessions | Move batch jobs and analytics workloads to async workers |

## Anti-Patterns

- Putting all analytics math directly inside route handlers
- Mixing raw CSV parsing and response rendering in one function
- Recomputing full model metrics on every dashboard load

---
*Architecture research for: sentiment analytics web application*
*Researched: 2026-04-02*
