# Testing Patterns

**Analysis Date:** 2026-04-01

## Test Framework

**Runner:**
- None configured in root project.
- No `pytest.ini`, `tox.ini`, or test dependencies in root `requirements.txt`.

**Assertion Library:**
- Not applicable (no automated tests found).

**Run Commands:**
```bash
# No automated test commands currently defined.
```

## Test File Organization

**Location:**
- No `tests/` directory in root.
- No root files matching `test_*.py` or `*_test.py`.

**Naming:**
- No established naming convention for tests yet.

## Test Structure

**Current reality:**
- Validation happens through manual browser and API checks.
- Health and prediction endpoints in `app.py` provide ad hoc runtime verification.

**Manual verification pattern:**
1. Start Flask or gunicorn process.
2. Open `/` and submit sample review text.
3. Call `/api/predict` with JSON payload.
4. Check `/health` for model readiness.

## Mocking

**Framework:**
- None configured.

**Current practice:**
- No mocking utilities present.
- Model artifacts are read directly from filesystem in runtime code.

## Fixtures and Factories

**Existing test data:**
- Example strings are embedded in templates (`templates/result.html` API example text).
- No dedicated fixture directory.

## Coverage

**Requirements:**
- No coverage target or reporting tool configured.

**Enforcement:**
- No CI gate for tests or coverage.

## Test Types

**Unit tests:**
- Not implemented.

**Integration tests:**
- Not implemented.

**E2E tests:**
- Not implemented.

## Common Risks from Current State

- Refactors can break request handlers without fast feedback.
- Model load edge cases may only be discovered at runtime.
- Behavior drift between root and nested duplicate app can go undetected.

## Suggested Baseline to Introduce

- Add `pytest` and create `tests/test_app.py`.
- Start with endpoint smoke tests for `/health`, `/api/predict`, and form route validation.
- Add one regression test for model unavailable behavior.

---

*Testing analysis: 2026-04-01*
*Update when test patterns change*
