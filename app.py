from flask import Flask, jsonify, redirect, render_template, request, url_for
from pathlib import Path
import logging
import os
import pickle

from storage import HistoryStore


BASE_DIR = Path(__file__).resolve().parent
APP_NAME = os.getenv("APP_NAME", "IMDB Sentiment Analysis")
APP_AUTHOR = os.getenv("APP_AUTHOR", "Your Name")
MAX_REVIEW_CHARS = int(os.getenv("MAX_REVIEW_CHARS", "2000"))
MAX_CONTENT_LENGTH = int(os.getenv("MAX_CONTENT_LENGTH", "16384"))
HISTORY_DB_PATH = Path(
    os.getenv("HISTORY_DB_PATH", BASE_DIR / "data" / "history.db")
).resolve()
ENABLE_SWAGGER = os.getenv("ENABLE_SWAGGER", "0") == "1"

logging.basicConfig(level=os.getenv("LOG_LEVEL", "INFO"))
logger = logging.getLogger("imdb-sentiment-app")

app = Flask(__name__)
app.config["MAX_REVIEW_CHARS"] = MAX_REVIEW_CHARS
app.config["MAX_CONTENT_LENGTH"] = MAX_CONTENT_LENGTH
app.config["APP_NAME"] = APP_NAME
app.config["APP_AUTHOR"] = APP_AUTHOR
app.config["HISTORY_DB_PATH"] = str(HISTORY_DB_PATH)

if ENABLE_SWAGGER:
    try:
        from flasgger import Swagger
    except ImportError:
        logger.warning("Swagger enabled but flasgger is not installed.")
    else:
        Swagger(app)

MODEL_PATH = Path(os.getenv("MODEL_PATH", BASE_DIR / "Naive_Bayes_model_imdb.pkl")).resolve()
VECTORIZER_PATH = Path(os.getenv("VECTORIZER_PATH", BASE_DIR / "countVect_imdb.pkl")).resolve()


def load_pickle(path: Path):
    with path.open("rb") as handle:
        return pickle.load(handle)


def load_artifacts():
    try:
        model = load_pickle(MODEL_PATH)
        vectorizer = load_pickle(VECTORIZER_PATH)
        return model, vectorizer, None
    except Exception as exc:
        return None, None, f"{type(exc).__name__}: {exc}"


model, vectorizer, model_error = load_artifacts()
if model_error:
    logger.error("Model load failed: %s", model_error)

history_store = HistoryStore(app.config["HISTORY_DB_PATH"])
try:
    history_store.init_schema()
except Exception as exc:
    logger.error("History schema init failed: %s", exc)


def ensure_model_loaded():
    global model, vectorizer, model_error
    if model is None or vectorizer is None:
        model, vectorizer, model_error = load_artifacts()
        if model_error:
            logger.error("Model load failed: %s", model_error)
    return model, vectorizer, model_error


def base_context(**extra):
    context = {
        "app_name": app.config["APP_NAME"],
        "author": app.config["APP_AUTHOR"],
        "max_chars": app.config["MAX_REVIEW_CHARS"],
    }
    context.update(extra)
    return context


def validate_review(review: str):
    cleaned = (review or "").strip()
    if not cleaned:
        return None, "Please enter a review."
    if len(cleaned) > app.config["MAX_REVIEW_CHARS"]:
        return (
            None,
            f"Please keep reviews under {app.config['MAX_REVIEW_CHARS']} characters.",
        )
    return cleaned, None


def predict_sentiment(review: str):
    vector = vectorizer.transform([review])
    prediction = int(model.predict(vector)[0])
    label = "Positive" if prediction == 1 else "Negative"
    confidence = None
    if hasattr(model, "predict_proba"):
        confidence = float(model.predict_proba(vector)[0][prediction])
    return {"value": prediction, "label": label, "confidence": confidence}


def wants_json_response():
    if request.path.startswith("/api/"):
        return True
    best = request.accept_mimetypes.best
    return best == "application/json"


@app.after_request
def add_security_headers(response):
    response.headers.setdefault("X-Content-Type-Options", "nosniff")
    response.headers.setdefault("X-Frame-Options", "DENY")
    response.headers.setdefault("Referrer-Policy", "no-referrer")
    response.headers.setdefault("Permissions-Policy", "geolocation=(), microphone=()")
    return response


@app.get("/")
def home():
    return render_template("home.html", **base_context(review="", error=None))


@app.get("/predict")
def predict_get():
    return redirect(url_for("home"))


@app.post("/predict")
def predict_post():
    _, _, current_error = ensure_model_loaded()
    if current_error:
        return render_template(
            "home.html",
            **base_context(
                review="",
                error="The model is not ready. Check server logs and verify the model files.",
            ),
        )

    review_input = request.form.get("Reviews", "")
    review, error = validate_review(review_input)
    if error:
        return render_template(
            "home.html",
            **base_context(error=error, review=review or review_input),
        )

    result = predict_sentiment(review)
    confidence_value = result["confidence"]
    if confidence_value is not None:
        confidence_pct = f"{confidence_value * 100:.1f}%"
        confidence_percent = int(round(confidence_value * 100))
    else:
        confidence_pct = None
        confidence_percent = 50
    return render_template(
        "result.html",
        **base_context(
            review=review,
            result=result,
            confidence_pct=confidence_pct,
            confidence_percent=confidence_percent,
        ),
    )


@app.post("/api/predict")
def api_predict():
    _, _, current_error = ensure_model_loaded()
    if current_error:
        return jsonify({"error": "model_unavailable"}), 503

    payload = request.get_json(silent=True) or {}
    review, error = validate_review(payload.get("review", ""))
    if error:
        return jsonify({"error": error}), 400

    result = predict_sentiment(review)
    response = {
        "label": result["label"],
        "value": result["value"],
        "confidence": result["confidence"],
    }
    return jsonify(response)


@app.get("/health")
def health():
    _, _, current_error = ensure_model_loaded()
    if current_error:
        return jsonify({"status": "error", "detail": current_error}), 503
    return jsonify({"status": "ok"}), 200


@app.errorhandler(404)
def not_found(_error):
    if wants_json_response():
        return jsonify({"error": "not_found"}), 404
    return (
        render_template(
            "home.html",
            **base_context(error="Page not found.", review=""),
        ),
        404,
    )


@app.errorhandler(500)
def server_error(_error):
    if wants_json_response():
        return jsonify({"error": "server_error"}), 500
    return (
        render_template(
            "home.html",
            **base_context(error="Something went wrong. Please try again.", review=""),
        ),
        500,
    )


@app.errorhandler(413)
def request_too_large(_error):
    if wants_json_response():
        return jsonify({"error": "request_too_large"}), 413
    return (
        render_template(
            "home.html",
            **base_context(
                error="Review too large. Please shorten your text and try again.",
                review="",
            ),
        ),
        413,
    )


if __name__ == "__main__":
    debug = os.getenv("FLASK_DEBUG", "0") == "1"
    port = int(os.getenv("PORT", "5000"))
    app.run(host="0.0.0.0", port=port, debug=debug)
    
