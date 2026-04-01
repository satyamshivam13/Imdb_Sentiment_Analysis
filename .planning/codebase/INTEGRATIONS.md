# External Integrations

**Analysis Date:** 2026-04-01

## APIs and External Services

**External APIs:**
- None detected in application code.
- Inference is fully local through pickled model artifacts.

**Email, SMS, Payments, Third-party auth:**
- None detected.

## Data Storage

**Databases:**
- No relational or NoSQL database integration found.

**File Storage:**
- Local file system only.
  - `Naive_Bayes_model_imdb.pkl` - trained classifier
  - `countVect_imdb.pkl` - text vectorizer
- Static assets served from `static/`.

**Caching:**
- No Redis or external cache configured.

## Authentication and Identity

**Auth Provider:**
- No user authentication or identity provider integration.

**Sessions and Accounts:**
- App behavior is anonymous and stateless per request.

## Monitoring and Observability

**Error Tracking:**
- No Sentry, Rollbar, or equivalent integration.

**Analytics:**
- No product analytics integration found.

**Logs:**
- Python logging configured in `app.py` using standard library logging.
- Output destination appears to be process stdout/stderr.

## CI/CD and Deployment

**Hosting Pattern:**
- `Procfile` uses `web: gunicorn app:app` for PaaS-style deployment.

**CI Pipeline:**
- No GitHub Actions or other CI config files detected.

## Environment Configuration

**Development:**
- Configuration via environment variables in `app.py`.
- Model paths can be overridden with `MODEL_PATH` and `VECTORIZER_PATH`.

**Staging and Production:**
- No dedicated environment-specific config files found.
- Same code path likely used for all environments with different env vars.

## Webhooks and Callbacks

**Incoming webhooks:**
- None.

**Outgoing callbacks/webhooks:**
- None.

## Integration Notes

- Optional Swagger support relies on `flasgger` and `ENABLE_SWAGGER=1`.
- Nested repo copy has a broader dependency list in `Imdb-Sentiment-Analysis-Flask/requirements.txt`, including data science packages not required by the root runtime.

---

*Integration audit: 2026-04-01*
*Update when adding or removing external services*
