# Codebase Concerns

**Analysis Date:** 2026-04-01

## Tech Debt

**Duplicate project trees:**
- Issue: Two app copies exist (`app.py` and `Imdb-Sentiment-Analysis-Flask/app.py`) with behavioral drift.
- Why: Nested directory appears to be a copied earlier version.
- Impact: Fixes can land in one copy and silently miss the other.
- Fix approach: Choose one canonical app root and remove/archive the duplicate.

**Single-module backend design:**
- Issue: Routing, validation, artifact loading, and inference all live in `app.py`.
- Why: Fast initial implementation.
- Impact: Growing feature work becomes harder to reason about and test.
- Fix approach: Split into modules (`routes`, `services`, `config`, `inference`).

## Known Bugs and Behavioral Risks

**Stale model state risk in nested app copy:**
- Symptoms: If model files are unavailable at startup, nested app may stay unavailable without retry.
- Trigger: Missing/corrupt `.pkl` files when process starts in nested copy.
- Workaround: Restart service after correcting files.
- Root cause: Nested app version does not include `ensure_model_loaded` retry path.

**Version drift between manifests:**
- Symptoms: Running from root versus nested directory can install different package sets.
- Trigger: Using `requirements.txt` in different locations.
- Workaround: Standardize execution from one project root.
- Root cause: Duplicate manifests with different contents.

## Security Considerations

**Pickle loading trust boundary:**
- Risk: `pickle.load` executes arbitrary code if artifact files are tampered.
- Files: `app.py`, model artifacts in project root.
- Current mitigation: None beyond local file access assumptions.
- Recommendations: Restrict write access to artifact files and validate artifact provenance.

**No request throttling on inference endpoint:**
- Risk: `/api/predict` can be abused for denial-of-service style traffic spikes.
- Current mitigation: Payload size limit and text length validation.
- Recommendations: Add rate limiting and upstream request controls.

## Performance Bottlenecks

**Synchronous prediction path:**
- Problem: Each request performs vectorization and prediction inline.
- Measurement: No benchmark data found in repo.
- Cause: Single-threaded request handling path for inference.
- Improvement path: Add lightweight load tests and tune worker count in gunicorn.

**Large repository footprint:**
- Problem: Committed `venv/` and model binaries increase repo size and clone time.
- Files: `Imdb-Sentiment-Analysis-Flask/venv/`, `*.pkl`.
- Cause: Environment and artifacts committed directly.
- Improvement path: Add `.gitignore`, move heavy artifacts to controlled storage when appropriate.

## Fragile Areas

**Template and route coupling:**
- Why fragile: Form field names (`Reviews`) and template variables must match route logic exactly.
- Files: `templates/home.html`, `app.py`.
- Common failures: Renaming form fields without backend updates causes silent validation failures.
- Safe modification: Change template and route handler together and smoke-test `/predict`.
- Test coverage: No automated tests currently.

**Mixed API and HTML error behavior:**
- Why fragile: Root app has content-type aware error behavior, nested copy is simpler.
- Files: `app.py`, `Imdb-Sentiment-Analysis-Flask/app.py`.
- Common failures: Inconsistent responses depending on which app is run.
- Safe modification: Consolidate to one app module, then standardize response policy.

## Scaling Limits

**Compute scaling:**
- Current capacity: Not documented; depends on gunicorn worker/process settings.
- Limit: CPU-bound inference in each worker can saturate quickly under burst traffic.
- Symptoms at limit: Rising response times and worker timeouts.
- Scaling path: Increase workers, add autoscaling, or introduce async queueing if throughput grows.

## Dependencies at Risk

**Older Flask stack:**
- Risk: `Flask==2.1.2` and related pins may miss newer fixes and compatibility improvements.
- Impact: Security and maintenance burden over time.
- Migration plan: Evaluate upgrade path to current Flask/LTS-compatible dependency set.

## Missing Critical Features

**No automated regression testing:**
- Problem: Core inference and route behavior have no test safety net.
- Current workaround: Manual checks via browser and ad hoc API calls.
- Blocks: Safe refactoring and fast change validation.
- Implementation complexity: Low to medium for initial pytest smoke suite.

**No CI validation workflow:**
- Problem: Commits are not automatically checked for syntax, tests, or dependency issues.
- Current workaround: Manual local runs.
- Blocks: Reliable team collaboration and deployment confidence.
- Implementation complexity: Medium.

## Test Coverage Gaps

**Endpoint contracts untested:**
- What is not tested: `/api/predict`, `/health`, and HTML post flow for success and errors.
- Risk: Breaking API response shape or user flow without detection.
- Priority: High.

**Error pathways untested:**
- What is not tested: model unavailable behavior and oversized payload handling.
- Risk: Runtime failures in edge cases.
- Priority: High.

---

*Concerns audit: 2026-04-01*
*Update as issues are fixed or new ones discovered*
