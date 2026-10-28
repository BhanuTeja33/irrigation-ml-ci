import logging
import sys
import time
import uuid
from pathlib import Path

import joblib
import pandas as pd
from flask import Flask, Response, jsonify, request
from prometheus_client import (
    CONTENT_TYPE_LATEST,
    Counter,
    Gauge,
    Histogram,
    generate_latest,
)

# Configure application logger to stdout
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
    force=True,
)
logger = logging.getLogger("irrigation-api")

app = Flask(__name__)

# --- Prometheus Metrics Definitions ---
HTTP_REQUESTS = Counter(
    "irrigation_api_http_requests_total",
    "Total HTTP requests received by the Irrigation Need Prediction API",
    ["method", "path", "status"],
)
HTTP_LATENCY = Histogram(
    "irrigation_api_http_request_duration_seconds",
    "HTTP request duration in seconds",
    ["method", "path"],
)
PREDICTIONS = Counter(
    "irrigation_api_predictions_total",
    "Total Irrigation Need Prediction attempts",
    ["result"],
)
MODEL_LOADED = Gauge(
    "irrigation_api_model_loaded",
    "Whether the Irrigation Need Prediction model is loaded (1=loaded, 0=not loaded)",
)

MODEL_PATH = Path("irrigation_model.pkl")
FEATURES = [
    "soil_moisture",
    "temperature",
    "humidity",
    "rainfall_forecast_mm",
]

# Non-sensitive features approved for logging
SAFE_INPUT_FIELDS = set(FEATURES)


def load_model():
    if not MODEL_PATH.exists():
        MODEL_LOADED.set(0)
        logger.error("event=model_missing model_file=%s", MODEL_PATH)
        raise FileNotFoundError(
            "irrigation_model.pkl was not found. "
            "Run the training pipeline first."
        )
    try:
        model = joblib.load(MODEL_PATH)
        MODEL_LOADED.set(1)
        logger.info("event=model_loaded model_file=%s", MODEL_PATH)
        return model
    except Exception:
        MODEL_LOADED.set(0)
        logger.exception("event=model_load_failed model_file=%s", MODEL_PATH)
        raise


# Load model on startup
try:
    model = load_model()
except Exception as e:
    logger.warning("Startup model load skipped or deferred: %s", e)
    model = None


@app.before_request
def start_timer():
    request.environ["start_time"] = time.perf_counter()
    request.environ["request_id"] = request.headers.get("X-Request-ID", str(uuid.uuid4()))


@app.after_request
def log_and_record_metrics(response):
    start = request.environ.get("start_time", time.perf_counter())
    request_id = request.environ.get("request_id", "unknown")
    duration = time.perf_counter() - start
    duration_ms = duration * 1000

    path = request.path
    method = request.method
    status_code = response.status_code

    # Do not count /metrics scrape requests in application traffic metrics
    if path != "/metrics":
        HTTP_REQUESTS.labels(
            method=method,
            path=path,
            status=str(status_code),
        ).inc()
        HTTP_LATENCY.labels(
            method=method,
            path=path,
        ).observe(duration)

    level = logging.WARNING if status_code >= 400 else logging.INFO
    logger.log(
        level,
        "event=http_request request_id=%s method=%s path=%s status=%s duration_ms=%.2f",
        request_id,
        method,
        path,
        status_code,
        duration_ms,
    )
    response.headers["X-Request-ID"] = request_id
    return response


@app.get("/")
def health_check():
    return jsonify({
        "status": "ok",
        "service": "irrigation-need-prediction"
    })


@app.get("/metrics")
def metrics():
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)


@app.post("/predict")
def predict():
    request_id = request.environ.get("request_id", "unknown")
    data = request.get_json(silent=True)

    if not data:
        logger.warning(
            "event=validation_error request_id=%s path=/predict reason=missing_json_body",
            request_id,
        )
        return jsonify({"error": "JSON request body is required"}), 400

    missing_fields = [
        feature for feature in FEATURES
        if feature not in data
    ]

    if missing_fields:
        logger.warning(
            "event=validation_error request_id=%s path=/predict missing_fields=%s",
            request_id,
            missing_fields,
        )
        return jsonify({
            "error": "Missing required fields",
            "missing_fields": missing_fields,
        }), 400

    try:
        safe_input = {
            k: data[k] for k in data if k in SAFE_INPUT_FIELDS
        }
        logger.info(
            "event=prediction_request request_id=%s feature_names=%s safe_input=%s",
            request_id,
            sorted(data.keys()),
            safe_input,
        )

        sample = pd.DataFrame([{
            feature: data[feature]
            for feature in FEATURES
        }])

        current_model = model or load_model()
        prediction_code = int(current_model.predict(sample)[0])
        prediction = "IRRIGATE" if prediction_code == 1 else "SKIP"

        PREDICTIONS.labels(result="success").inc()
        logger.info(
            "event=prediction_success request_id=%s prediction=%s prediction_code=%d",
            request_id,
            prediction,
            prediction_code,
        )

        return jsonify({
            "prediction": prediction,
            "prediction_code": prediction_code,
        })
    except Exception:
        PREDICTIONS.labels(result="error").inc()
        logger.exception("event=prediction_failed request_id=%s", request_id)
        return jsonify({"error": "Prediction failed"}), 500


@app.errorhandler(404)
def route_not_found(e):
    request_id = request.environ.get("request_id", "unknown")
    logger.warning("event=route_not_found request_id=%s path=%s", request_id, request.path)
    return jsonify({"error": "Route not found", "path": request.path}), 404


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
