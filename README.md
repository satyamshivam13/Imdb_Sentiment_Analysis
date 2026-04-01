# IMDb Sentiment Analysis (Flask)

A Flask-based sentiment analysis app for IMDb-style movie reviews with both single-review prediction and analytics-focused features.

## Features

- Single review sentiment prediction (web form + JSON API)
- Batch CSV sentiment analysis
- Batch report page with export support
- Dashboard with sentiment distribution and trend visualization
- Metrics observability page (model metrics from artifact)
- History archive with pagination and clear action
- Test coverage for core routes, batch flow, dashboard, metrics, and persistence

## Tech Stack

- Python 3.10+
- Flask
- scikit-learn
- Jinja templates
- SQLite (history/persistence)
- Chart.js (dashboard charts)
- pytest

## Project Structure

- `app.py` - Main Flask app and routes
- `services/` - Batch, history, and metrics service logic
- `storage/` - SQLite history store abstraction
- `templates/` - Jinja templates
- `static/` - CSS and JavaScript assets
- `tests/` - Automated test suite
- `data/model_metrics.json` - Metrics artifact used by observability page

## Setup

1. Clone the repository
2. Create and activate a virtual environment
3. Install dependencies
4. Run the app

### Windows (PowerShell)

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python app.py
```

App will be available at:

- http://127.0.0.1:5000

## Running Tests

```powershell
pytest -q
```

## Usage

### Single Prediction (Web)

- Open home page
- Enter a review
- Submit to get sentiment and confidence

### Single Prediction (API)

```bash
curl -X POST http://127.0.0.1:5000/api/predict \
  -H "Content-Type: application/json" \
  -d "{\"review\": \"This movie was fantastic!\"}"
```

### Batch CSV Analysis (Web)

- Upload a CSV from the home page
- Required review column aliases supported by service logic (for example: `review`, `reviews`, `review_text`, `text`)
- View batch report and download enriched results

### Batch CSV Analysis (API)

```bash
curl -X POST http://127.0.0.1:5000/api/batch/analyze \
  -F "reviews_file=@sample.csv"
```

## Important Files and Artifacts

- Model pickle: `Naive_Bayes_model_imdb.pkl`
- Vectorizer pickle: `countVect_imdb.pkl`
- Metrics artifact: `data/model_metrics.json`

## Deployment Notes

- `Procfile` and `Procfile.txt` are included for process startup compatibility.
- For production, use a WSGI server (for example Gunicorn) and proper environment configuration.

## Environment Variables

Commonly used variables in this project include:

- `PORT`
- `MODEL_PATH`
- `VECTORIZER_PATH`
- `MAX_REVIEW_CHARS`
- `MAX_CONTENT_LENGTH`
- `HISTORY_DB_PATH`
- `ENABLE_SWAGGER`

If not set, sensible defaults in the app are used.

## Notes

- Local runtime database files are ignored via `.gitignore` (`data/*.db`).
- Dataset CSV files are ignored by default to keep the repository lightweight.

## License

This project includes a `LICENSE` file in the repository root.
