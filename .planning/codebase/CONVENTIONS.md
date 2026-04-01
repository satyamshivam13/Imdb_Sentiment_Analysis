# Coding Conventions

**Analysis Date:** 2026-04-01

## Naming Patterns

**Files:**
- Top-level app entrypoint is `app.py`.
- Template names are page-oriented: `base.html`, `home.html`, `result.html`.
- Asset files are centralized as `static/css/app.css` and `static/js/app.js`.

**Functions:**
- Python helpers and route handlers use snake_case (`predict_sentiment`, `predict_post`).
- Flask routes are mapped with decorator + function pairs.

**Variables and constants:**
- Runtime constants are uppercase near top of file (`MODEL_PATH`, `MAX_REVIEW_CHARS`).
- General variables use snake_case (`model_error`, `confidence_pct`).

## Code Style

**Formatting:**
- No formatter config file detected (`black`, `ruff`, `autopep8` not configured).
- Python style mostly follows readable multi-line blocks and explicit returns.
- HTML style uses utility-heavy Tailwind class attributes.

**Linting:**
- No lint command or lint config detected in root project.

## Import Organization

**Observed order in `app.py`:**
1. Flask imports
2. Standard library imports (`pathlib`, `logging`, `os`, `pickle`)

**Notes:**
- Import grouping exists but strict style tooling is not enforced.

## Error Handling

**Patterns:**
- Input validation handled with helper `validate_review`.
- Artifact load failures captured in `model_error` and surfaced in responses.
- Root app includes Flask error handlers for `404`, `500`, and `413`.

**API behavior:**
- JSON routes return explicit error objects with proper status codes.

## Logging

**Framework:**
- Python standard library logging via `logging.basicConfig`.

**Patterns:**
- Startup/runtime model-load failures logged through named logger `imdb-sentiment-app`.
- No structured logging or request correlation IDs detected.

## Comments

**Code comments:**
- Minimal inline comments in Python source.
- Readability depends on function naming and clear branching.

**Template comments:**
- None significant; semantic grouping done through markup blocks.

## Function Design

**Size and shape:**
- Single `app.py` contains both helpers and route handlers.
- Helper functions are short and focused (validation, prediction, context).
- Route handlers combine validation, inference call, and response shaping.

**Return strategy:**
- Explicit return tuples for Flask responses with status codes where needed.

## Module Design

**Current pattern:**
- Monolithic module pattern in root `app.py`.
- No package-level separation for routes, services, or config.

**Frontend split:**
- Presentation concerns split across templates and static assets.

## Practical Guidance for New Code

- Match snake_case for Python function and variable names.
- Keep input validation in helper functions, then call from routes.
- Continue dual-surface pattern: browser-friendly HTML plus JSON API clarity.
- Prefer adding behavior to root app and root assets (not nested duplicate copy).

---

*Convention analysis: 2026-04-01*
*Update when patterns change*
