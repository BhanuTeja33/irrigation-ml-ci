from pathlib import Path
import json
import joblib
import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DRIFT_DIR = PROJECT_ROOT / "drift"
HISTORICAL = PROJECT_ROOT / "field_data.csv"
RECENT = DRIFT_DIR / "current_labeled_data.csv"
DRIFT_REPORT = DRIFT_DIR / "drift_report.json"
CANDIDATE_MODEL = DRIFT_DIR / "irrigation_model_candidate.pkl"
METRICS_FILE = DRIFT_DIR / "retraining_metrics.json"

FEATURES = [
    "soil_moisture",
    "temperature",
    "humidity",
    "rainfall_forecast_mm",
]
TARGET = "irrigate"

with open(DRIFT_REPORT, encoding="utf-8") as f:
    drift_report = json.load(f)

if not drift_report.get("overall_drift", False):
    print("=" * 60)
    print("DRIFT STATUS: NO OVERALL DRIFT DETECTED.")
    print("Retraining skipped - preserving existing production model.")
    print("=" * 60)
    raise SystemExit(0)

if not RECENT.exists():
    raise FileNotFoundError(
        "Drift was detected, but recent ground-truth data (current_labeled_data.csv) is missing."
    )

print("=" * 60)
print("DRIFT DETECTED -> INITIATING CANDIDATE MODEL RETRAINING")
print("=" * 60)

historical = pd.read_csv(HISTORICAL)
recent = pd.read_csv(RECENT)
required = FEATURES + [TARGET]

for name, frame in [("historical", historical), ("recent", recent)]:
    missing = [c for c in required if c not in frame.columns]
    if missing:
        raise ValueError(f"{name} data missing required columns: {missing}")

combined = pd.concat(
    [historical[required], recent[required]],
    ignore_index=True
).dropna(subset=[TARGET])

X = combined[FEATURES]
y = combined[TARGET]

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

candidate_pipeline = Pipeline([
    ("scaler", StandardScaler()),
    ("model", LogisticRegression(max_iter=1000, random_state=42))
])

candidate_pipeline.fit(X_train, y_train)
preds = candidate_pipeline.predict(X_test)

accuracy = accuracy_score(y_test, preds)
precision = precision_score(y_test, preds, zero_division=0)
recall = recall_score(y_test, preds, zero_division=0)
f1 = f1_score(y_test, preds, zero_division=0)

joblib.dump(candidate_pipeline, CANDIDATE_MODEL)

metrics = {
    "project": "Irrigation Need Prediction",
    "candidate_model_path": str(CANDIDATE_MODEL.name),
    "candidate_accuracy": round(float(accuracy), 4),
    "candidate_precision": round(float(precision), 4),
    "candidate_recall": round(float(recall), 4),
    "candidate_f1": round(float(f1), 4),
    "training_rows": int(len(X_train)),
    "test_rows": int(len(X_test)),
    "historical_rows": int(len(historical)),
    "recent_labeled_rows": int(len(recent)),
    "total_rows": int(len(combined)),
}

with open(METRICS_FILE, "w", encoding="utf-8") as f:
    json.dump(metrics, f, indent=2)

print("Retraining completed successfully.")
print(json.dumps(metrics, indent=2))
print("Candidate model saved to:", CANDIDATE_MODEL)
