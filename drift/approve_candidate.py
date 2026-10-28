from pathlib import Path
import json
import shutil
import joblib

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DRIFT_DIR = PROJECT_ROOT / "drift"
CANDIDATE = DRIFT_DIR / "irrigation_model_candidate.pkl"
METRICS = DRIFT_DIR / "retraining_metrics.json"
APPROVED = PROJECT_ROOT / "irrigation_model.pkl"
BACKUP = DRIFT_DIR / "irrigation_model_backup.pkl"

MIN_ACCURACY = 0.85

if not METRICS.exists() or not CANDIDATE.exists():
    raise FileNotFoundError("Retraining metrics or candidate model file not found.")

with open(METRICS, encoding="utf-8") as f:
    metrics = json.load(f)

accuracy = metrics["candidate_accuracy"]

print("=" * 60)
print("QUALITY GATE EVALUATION FOR CANDIDATE MODEL")
print("=" * 60)
print(f"Candidate Model Accuracy: {accuracy:.4f} ({accuracy * 100:.2f}%)")
print(f"Required Threshold      : {MIN_ACCURACY:.4f} ({MIN_ACCURACY * 100:.2f}%)")

if accuracy < MIN_ACCURACY:
    print("-" * 60)
    print("QUALITY GATE: FAIL")
    print(f"Candidate accuracy {accuracy:.4f} is below minimum acceptable threshold {MIN_ACCURACY:.4f}.")
    print("Action: Preserving current production model. Candidate rejected.")
    print("-" * 60)
    raise SystemExit(1)

# Backup current production model if it exists
if APPROVED.exists():
    shutil.copy2(APPROVED, BACKUP)
    print(f"Existing production model backed up to: {BACKUP.name}")

# Promote candidate model
shutil.copy2(CANDIDATE, APPROVED)

# Sanity check: confirm the promoted model loads cleanly
model = joblib.load(APPROVED)
sample_test = model.predict([[20, 38, 25, 0]])[0]

print("-" * 60)
print("QUALITY GATE: PASS")
print(f"Candidate model successfully promoted to production: {APPROVED}")
print(f"Sanity Check Inference Test: soil=20, temp=38, hum=25, rain=0 -> Prediction: {sample_test}")
print("-" * 60)
