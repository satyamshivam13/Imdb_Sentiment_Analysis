<!-- GSD:project-start source:PROJECT.md -->
## Project

**IMDb Sentiment Analytics Platform**

This project evolves an existing IMDb sentiment prediction Flask app into an analytics-focused product for internal and demo stakeholders. Instead of showing only a single prediction, it will surface sentiment patterns, model quality, and batch insights that are useful for presentations and decision discussions.

**Core Value:** Internal stakeholders can quickly understand sentiment trends and model quality from review data, not just single-review outputs.

### Constraints

- **Architecture**: Keep Flask backend and add a lightweight JavaScript chart stack (e.g., Chart.js) � chosen to increase capability without introducing SPA complexity.
- **Scope Size**: Balanced v1 with 4 feature tracks � enough breadth for a complete analytics story while keeping delivery practical.
- **User Focus**: Optimize first for internal/demo stakeholders � prioritize clarity, metrics visibility, and presentability.
- **Authentication**: Explicitly deferred from v1 � avoid non-core complexity while analytics foundation is built.
- **Inference Runtime**: Maintain compatibility with existing local pickle-based inference artifacts � preserve current prediction pipeline continuity.
<!-- GSD:project-end -->

<!-- GSD:stack-start source:codebase/STACK.md -->
## Technology Stack

## Languages
- Python 3.10 - Main server and inference logic in `app.py`
- HTML (Jinja templates) - Server-rendered UI in `templates/*.html`
- CSS - Custom styles in `static/css/app.css`
- JavaScript - Client-side UI behavior in `static/js/app.js`
## Runtime
- Python runtime (3.10 inferred from `Imdb-Sentiment-Analysis-Flask/venv/Scripts/python.exe`)
- WSGI process model via `gunicorn` in `Procfile`
- pip via `requirements.txt`
- Lockfile: none present
## Frameworks
- Flask 2.1.2 - Web framework for HTML pages and JSON endpoints
- Jinja2 (indirect via Flask) - HTML template rendering
- scikit-learn 1.1.3 - Model inference
- No automated test framework configured
- No frontend bundler; Tailwind loaded from CDN in `templates/base.html`
- Optional Swagger UI via `flasgger` when `ENABLE_SWAGGER=1`
## Key Dependencies
- `Flask==2.1.2` - HTTP routing and request handling
- `gunicorn==20.1.0` - Production WSGI server process
- `scikit-learn==1.1.3` - Naive Bayes model API (`predict`, `predict_proba`)
- `numpy==1.22.1` and `scipy==1.9.3` - ML runtime dependencies
- Pickled artifacts `Naive_Bayes_model_imdb.pkl` and `countVect_imdb.pkl` used at app startup
- Optional `flasgger==0.9.5` appears in nested manifest `Imdb-Sentiment-Analysis-Flask/requirements.txt`
## Configuration
- `APP_NAME`, `APP_AUTHOR`
- `MAX_REVIEW_CHARS`, `MAX_CONTENT_LENGTH`
- `MODEL_PATH`, `VECTORIZER_PATH`
- `ENABLE_SWAGGER`, `LOG_LEVEL`
- `PORT`, `FLASK_DEBUG`
- `requirements.txt`
- `Procfile` and `Procfile.txt`
- No Dockerfile, CI workflow, or typed config files found
## Platform Requirements
- Windows-friendly layout (paths and local `venv` copy present)
- Python + pip environment required
- Any host supporting `gunicorn app:app`
- File-system access to model and vectorizer `.pkl` artifacts
## Stack Notes
- There are two project copies:
- Nested copy includes `venv/`, which should usually be excluded from source control.
<!-- GSD:stack-end -->

<!-- GSD:conventions-start source:CONVENTIONS.md -->
## Conventions

## Naming Patterns
- Top-level app entrypoint is `app.py`.
- Template names are page-oriented: `base.html`, `home.html`, `result.html`.
- Asset files are centralized as `static/css/app.css` and `static/js/app.js`.
- Python helpers and route handlers use snake_case (`predict_sentiment`, `predict_post`).
- Flask routes are mapped with decorator + function pairs.
- Runtime constants are uppercase near top of file (`MODEL_PATH`, `MAX_REVIEW_CHARS`).
- General variables use snake_case (`model_error`, `confidence_pct`).
## Code Style
- No formatter config file detected (`black`, `ruff`, `autopep8` not configured).
- Python style mostly follows readable multi-line blocks and explicit returns.
- HTML style uses utility-heavy Tailwind class attributes.
- No lint command or lint config detected in root project.
## Import Organization
- Import grouping exists but strict style tooling is not enforced.
## Error Handling
- Input validation handled with helper `validate_review`.
- Artifact load failures captured in `model_error` and surfaced in responses.
- Root app includes Flask error handlers for `404`, `500`, and `413`.
- JSON routes return explicit error objects with proper status codes.
## Logging
- Python standard library logging via `logging.basicConfig`.
- Startup/runtime model-load failures logged through named logger `imdb-sentiment-app`.
- No structured logging or request correlation IDs detected.
## Comments
- Minimal inline comments in Python source.
- Readability depends on function naming and clear branching.
- None significant; semantic grouping done through markup blocks.
## Function Design
- Single `app.py` contains both helpers and route handlers.
- Helper functions are short and focused (validation, prediction, context).
- Route handlers combine validation, inference call, and response shaping.
- Explicit return tuples for Flask responses with status codes where needed.
## Module Design
- Monolithic module pattern in root `app.py`.
- No package-level separation for routes, services, or config.
- Presentation concerns split across templates and static assets.
## Practical Guidance for New Code
- Match snake_case for Python function and variable names.
- Keep input validation in helper functions, then call from routes.
- Continue dual-surface pattern: browser-friendly HTML plus JSON API clarity.
- Prefer adding behavior to root app and root assets (not nested duplicate copy).
<!-- GSD:conventions-end -->

<!-- GSD:architecture-start source:ARCHITECTURE.md -->
## Architecture

## Pattern Overview
- Single-process web server pattern (`gunicorn app:app`)
- Mixed interface surface: HTML views plus JSON API endpoints
- Local model inference from pickled artifacts
- No separate service, queue, or database layers
## Layers
- Purpose: Render pages and provide browser interactions.
- Contains: `templates/base.html`, `templates/home.html`, `templates/result.html`, `static/css/app.css`, `static/js/app.js`
- Depends on: Flask route context variables
- Used by: Browser clients
- Purpose: Route requests, validate inputs, and shape responses.
- Contains: Flask route handlers in `app.py` (`/`, `/predict`, `/api/predict`, `/health`)
- Depends on: ML inference helpers and validation helpers
- Used by: Browsers and API clients
- Purpose: Transform review text and compute sentiment prediction.
- Contains: `load_artifacts`, `validate_review`, `predict_sentiment` in `app.py`
- Depends on: pickled model/vectorizer and scikit-learn interfaces
- Used by: `/predict` and `/api/predict` handlers
- Purpose: Provide runtime artifacts and static resources.
- Contains: `Naive_Bayes_model_imdb.pkl`, `countVect_imdb.pkl`, static files
- Depends on: file system paths and environment configuration
- Used by: Inference and template/static serving
## Data Flow
- Process-level model state loaded on startup and refreshed on demand in the root app.
- Request handling is otherwise stateless.
## Key Abstractions
- Purpose: Consolidate template context defaults.
- Example: `base_context` helper in root `app.py`
- Pattern: helper function for shared render context
- Purpose: Centralize model/vectorizer load behavior and error capture.
- Example: `load_artifacts` and `ensure_model_loaded` in root `app.py`
- Pattern: lazy retry + shared process globals
- Purpose: Serve both browser and API clients.
- Example: HTML endpoints and `/api/*` endpoints in same module
- Pattern: route-level branching by endpoint and content type expectations
## Entry Points
- Location: `app.py`
- Triggers: `gunicorn app:app` and direct `python app.py`
- Responsibilities: app creation, route registration, inference wiring
- Location: `Imdb-Sentiment-Analysis-Flask/app.py`
- Triggers: independent execution in nested directory
- Responsibilities: similar behavior with fewer safety features
## Error Handling
- Input validation errors return form re-render (HTML) or HTTP 400 (JSON)
- Model load failures return service-unavailable style responses
- Root app includes handlers for `404`, `500`, and `413`
## Cross-Cutting Concerns
- Standard library logging configured in `app.py`.
- `validate_review` enforces non-empty and max-length constraints.
- Root `app.py` uses `@app.after_request` to set baseline response headers.
<!-- GSD:architecture-end -->

<!-- GSD:workflow-start source:GSD defaults -->
## GSD Workflow Enforcement

Before using Edit, Write, or other file-changing tools, start work through a GSD command so planning artifacts and execution context stay in sync.

Use these entry points:
- `/gsd:quick` for small fixes, doc updates, and ad-hoc tasks
- `/gsd:debug` for investigation and bug fixing
- `/gsd:execute-phase` for planned phase work

Do not make direct repo edits outside a GSD workflow unless the user explicitly asks to bypass it.
<!-- GSD:workflow-end -->



<!-- GSD:profile-start -->
## Developer Profile

> Profile not yet configured. Run `/gsd:profile-user` to generate your developer profile.
> This section is managed by `generate-claude-profile` -- do not edit manually.
<!-- GSD:profile-end -->
