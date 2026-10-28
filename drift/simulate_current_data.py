from pathlib import Path
import argparse
import numpy as np
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DRIFT_DIR = PROJECT_ROOT / "drift"
REFERENCE = DRIFT_DIR / "reference_data.csv"
OUTPUT = DRIFT_DIR / "current_data.csv"
LABELED_OUTPUT = DRIFT_DIR / "current_labeled_data.csv"

FEATURES = [
    "soil_moisture",
    "temperature",
    "humidity",
    "rainfall_forecast_mm",
]

parser = argparse.ArgumentParser(description="Simulate current production telemetry data")
parser.add_argument(
    "--mode",
    choices=["stable", "drift"],
    default="stable",
    help="Simulation mode: stable (no drift) or drift (environmental shift)"
)
args = parser.parse_args()

rng = np.random.default_rng(42)
reference = pd.read_csv(REFERENCE)
n = min(150, len(reference))
current = reference.sample(n=n, replace=True, random_state=42).reset_index(drop=True)

# Add small random noise for both modes
for feature in FEATURES:
    current[feature] = current[feature] + rng.normal(0, 1.0, size=len(current))

if args.mode == "drift":
    # Simulate a severe heatwave / drought event:
    # Soil moisture drops significantly, temperature spikes, humidity drops
    current["soil_moisture"] -= 18
    current["temperature"] += 8
    current["humidity"] -= 15
    current["rainfall_forecast_mm"] -= 4

# Clip values to physically realistic telemetry bounds
current["soil_moisture"] = current["soil_moisture"].clip(5, 95)
current["temperature"] = current["temperature"].clip(5, 55)
current["humidity"] = current["humidity"].clip(10, 100)
current["rainfall_forecast_mm"] = current["rainfall_forecast_mm"].clip(0, 100)

# Round values
for feature in FEATURES:
    current[feature] = current[feature].round(1)

# Save unlabeled production batch (for drift detection)
current.to_csv(OUTPUT, index=False)
print(f"Current telemetry batch generated in '{args.mode}' mode.")
print("Rows:", len(current))
print("File:", OUTPUT)

# Also generate ground-truth labels for retraining demonstration
# Rule: Low soil moisture or high temperature increases need for irrigation
labeled = current.copy()
score = (
    (100 - labeled["soil_moisture"]) * 0.45 +
    labeled["temperature"] * 0.35 +
    (100 - labeled["humidity"]) * 0.15 -
    labeled["rainfall_forecast_mm"] * 0.30
)
labeled["irrigate"] = (score >= 48).astype(int)
labeled.to_csv(LABELED_OUTPUT, index=False)
print("Recent labeled ground-truth dataset saved:", LABELED_OUTPUT)
