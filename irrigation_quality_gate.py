import json
import sys

MINIMUM_ACCURACY = 0.90

print("Reading irrigation model metrics...")

with open("metrics.json", "r") as file:
    metrics = json.load(file)

accuracy = metrics["accuracy"]

print("Model Accuracy   :", round(accuracy, 4))
print("Required Accuracy:", MINIMUM_ACCURACY)
print("Test Records     :", metrics["testing_records"])

if accuracy < MINIMUM_ACCURACY:
    print("IRRIGATION QUALITY GATE FAILED")
    print("Model accuracy is below the required threshold.")
    sys.exit(1)

print("IRRIGATION QUALITY GATE PASSED")
print("Model accuracy satisfies the required threshold.")
sys.exit(0)
