import json

import joblib
import numpy as np
import pandas as pd

from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler


def create_dataset():
    rng = np.random.default_rng(2026)
    number_of_fields = 400

    data = pd.DataFrame({
        "soil_moisture": rng.integers(10, 81, number_of_fields),
        "temperature": rng.integers(10, 46, number_of_fields),
        "humidity": rng.integers(20, 96, number_of_fields),
        "rainfall_forecast_mm": rng.integers(0, 31, number_of_fields)
    })

    # Higher score = field needs water more urgently
    data["irrigation_need_score"] = (
        0.50 * (100 - data["soil_moisture"])
        + 0.80 * data["temperature"]
        + 0.15 * (100 - data["humidity"])
        - 1.00 * data["rainfall_forecast_mm"]
    )

    # 1 = IRRIGATE, 0 = SKIP
    data["irrigate"] = (data["irrigation_need_score"] >= 45).astype(int)
    return data


def train_model():
    print("Creating dataset...")
    data = create_dataset()
    data.to_csv("field_data.csv", index=False)

    print("Dataset created successfully.")
    print("Number of records:", len(data))

    features = ["soil_moisture", "temperature", "humidity", "rainfall_forecast_mm"]

    X = data[features]
    y = data["irrigate"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, random_state=2026, stratify=y
    )

    print("Training records:", len(X_train))
    print("Testing records :", len(X_test))

    model = Pipeline([
        ("scaler", StandardScaler()),
        ("classifier", LogisticRegression(max_iter=1000, random_state=2026))
    ])

    print("Training model...")
    model.fit(X_train, y_train)

    predictions = model.predict(X_test)
    accuracy = accuracy_score(y_test, predictions)
    matrix = confusion_matrix(y_test, predictions)

    print("\nModel Evaluation")
    print("----------------")
    print("Accuracy:", round(accuracy, 4))
    print("\nConfusion Matrix:")
    print(matrix)

    joblib.dump(model, "irrigation_model.pkl")
    print("\nModel saved as irrigation_model.pkl")

    metrics = {
        "accuracy": float(accuracy),
        "training_records": len(X_train),
        "testing_records": len(X_test)
    }

    with open("metrics.json", "w") as file:
        json.dump(metrics, file, indent=4)

    print("Metrics saved as metrics.json")
    return accuracy


if __name__ == "__main__":
    train_model()
