# Technology Stack

**Analysis Date:** 2026-04-01

## Languages

**Primary:**
- Python 3.10 - Main server and inference logic in `app.py`

**Secondary:**
- HTML (Jinja templates) - Server-rendered UI in `templates/*.html`
- CSS - Custom styles in `static/css/app.css`
- JavaScript - Client-side UI behavior in `static/js/app.js`

## Runtime

**Environment:**
- Python runtime (3.10 inferred from `Imdb-Sentiment-Analysis-Flask/venv/Scripts/python.exe`)
- WSGI process model via `gunicorn` in `Procfile`

**Package Manager:**
- pip via `requirements.txt`
- Lockfile: none present

## Frameworks

**Core:**
- Flask 2.1.2 - Web framework for HTML pages and JSON endpoints
- Jinja2 (indirect via Flask) - HTML template rendering
- scikit-learn 1.1.3 - Model inference

**Testing:**
- No automated test framework configured

**Build/Dev:**
- No frontend bundler; Tailwind loaded from CDN in `templates/base.html`
- Optional Swagger UI via `flasgger` when `ENABLE_SWAGGER=1`

## Key Dependencies

**Critical:**
- `Flask==2.1.2` - HTTP routing and request handling
- `gunicorn==20.1.0` - Production WSGI server process
- `scikit-learn==1.1.3` - Naive Bayes model API (`predict`, `predict_proba`)
- `numpy==1.22.1` and `scipy==1.9.3` - ML runtime dependencies

**Infrastructure:**
- Pickled artifacts `Naive_Bayes_model_imdb.pkl` and `countVect_imdb.pkl` used at app startup
- Optional `flasgger==0.9.5` appears in nested manifest `Imdb-Sentiment-Analysis-Flask/requirements.txt`

## Configuration

**Environment:**
- `APP_NAME`, `APP_AUTHOR`
- `MAX_REVIEW_CHARS`, `MAX_CONTENT_LENGTH`
- `MODEL_PATH`, `VECTORIZER_PATH`
- `ENABLE_SWAGGER`, `LOG_LEVEL`
- `PORT`, `FLASK_DEBUG`

**Build and runtime files:**
- `requirements.txt`
- `Procfile` and `Procfile.txt`
- No Dockerfile, CI workflow, or typed config files found

## Platform Requirements

**Development:**
- Windows-friendly layout (paths and local `venv` copy present)
- Python + pip environment required

**Production:**
- Any host supporting `gunicorn app:app`
- File-system access to model and vectorizer `.pkl` artifacts

## Stack Notes

- There are two project copies:
  - Root application (actively improved version) at `app.py`
  - Nested copy at `Imdb-Sentiment-Analysis-Flask/app.py`
- Nested copy includes `venv/`, which should usually be excluded from source control.

---

*Stack analysis: 2026-04-01*
*Update after major dependency changes*
