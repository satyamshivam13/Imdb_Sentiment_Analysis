# Architecture

**Analysis Date:** 2026-04-01

## Pattern Overview

**Overall:** Monolithic Flask web app with server-rendered UI and local ML inference.

**Key Characteristics:**
- Single-process web server pattern (`gunicorn app:app`)
- Mixed interface surface: HTML views plus JSON API endpoints
- Local model inference from pickled artifacts
- No separate service, queue, or database layers

## Layers

**Presentation Layer:**
- Purpose: Render pages and provide browser interactions.
- Contains: `templates/base.html`, `templates/home.html`, `templates/result.html`, `static/css/app.css`, `static/js/app.js`
- Depends on: Flask route context variables
- Used by: Browser clients

**HTTP and Routing Layer:**
- Purpose: Route requests, validate inputs, and shape responses.
- Contains: Flask route handlers in `app.py` (`/`, `/predict`, `/api/predict`, `/health`)
- Depends on: ML inference helpers and validation helpers
- Used by: Browsers and API clients

**Inference Layer:**
- Purpose: Transform review text and compute sentiment prediction.
- Contains: `load_artifacts`, `validate_review`, `predict_sentiment` in `app.py`
- Depends on: pickled model/vectorizer and scikit-learn interfaces
- Used by: `/predict` and `/api/predict` handlers

**Resource Layer:**
- Purpose: Provide runtime artifacts and static resources.
- Contains: `Naive_Bayes_model_imdb.pkl`, `countVect_imdb.pkl`, static files
- Depends on: file system paths and environment configuration
- Used by: Inference and template/static serving

## Data Flow

**HTML Flow (`POST /predict`):**
1. Browser submits review form from `templates/home.html`.
2. `predict_post` validates input length and emptiness.
3. Model/vectorizer generate class and confidence.
4. Route renders `templates/result.html` with prediction context.

**API Flow (`POST /api/predict`):**
1. Client sends JSON payload `{"review": "..."}`.
2. `api_predict` parses JSON and validates review text.
3. Inference helpers run prediction.
4. JSON response returns label, numeric value, and confidence.

**State Management:**
- Process-level model state loaded on startup and refreshed on demand in the root app.
- Request handling is otherwise stateless.

## Key Abstractions

**Context Assembly:**
- Purpose: Consolidate template context defaults.
- Example: `base_context` helper in root `app.py`
- Pattern: helper function for shared render context

**Artifact Loading:**
- Purpose: Centralize model/vectorizer load behavior and error capture.
- Example: `load_artifacts` and `ensure_model_loaded` in root `app.py`
- Pattern: lazy retry + shared process globals

**Response Duality:**
- Purpose: Serve both browser and API clients.
- Example: HTML endpoints and `/api/*` endpoints in same module
- Pattern: route-level branching by endpoint and content type expectations

## Entry Points

**Application Module:**
- Location: `app.py`
- Triggers: `gunicorn app:app` and direct `python app.py`
- Responsibilities: app creation, route registration, inference wiring

**Nested Legacy Copy:**
- Location: `Imdb-Sentiment-Analysis-Flask/app.py`
- Triggers: independent execution in nested directory
- Responsibilities: similar behavior with fewer safety features

## Error Handling

**Strategy:** Route-level checks plus Flask error handlers.

**Patterns:**
- Input validation errors return form re-render (HTML) or HTTP 400 (JSON)
- Model load failures return service-unavailable style responses
- Root app includes handlers for `404`, `500`, and `413`

## Cross-Cutting Concerns

**Logging:**
- Standard library logging configured in `app.py`.

**Validation:**
- `validate_review` enforces non-empty and max-length constraints.

**Security Headers:**
- Root `app.py` uses `@app.after_request` to set baseline response headers.

---

*Architecture analysis: 2026-04-01*
*Update when major patterns change*
