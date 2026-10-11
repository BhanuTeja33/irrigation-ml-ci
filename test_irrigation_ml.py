import json
import os
import unittest

import joblib
import pandas as pd


class TestIrrigationMLPipeline(unittest.TestCase):

    def test_dataset_created(self):
        self.assertTrue(os.path.exists("field_data.csv"))

    def test_model_created(self):
        self.assertTrue(os.path.exists("irrigation_model.pkl"))

    def test_metrics_created(self):
        self.assertTrue(os.path.exists("metrics.json"))

    def test_accuracy_is_valid(self):
        with open("metrics.json", "r") as file:
            metrics = json.load(file)

        accuracy = metrics["accuracy"]
        self.assertGreaterEqual(accuracy, 0.0)
        self.assertLessEqual(accuracy, 1.0)

    def test_model_prediction(self):
        model = joblib.load("irrigation_model.pkl")

        sample = pd.DataFrame([{
            "soil_moisture": 40,
            "temperature": 30,
            "humidity": 60,
            "rainfall_forecast_mm": 5
        }])

        prediction = model.predict(sample)[0]
        self.assertIn(int(prediction), [0, 1])

    def test_dry_hot_field_needs_irrigation(self):
        model = joblib.load("irrigation_model.pkl")

        sample = pd.DataFrame([{
            "soil_moisture": 15,
            "temperature": 38,
            "humidity": 30,
            "rainfall_forecast_mm": 0
        }])

        prediction = model.predict(sample)[0]
        self.assertEqual(int(prediction), 1)

    def test_wet_cool_field_skips_irrigation(self):
        model = joblib.load("irrigation_model.pkl")

        sample = pd.DataFrame([{
            "soil_moisture": 75,
            "temperature": 15,
            "humidity": 85,
            "rainfall_forecast_mm": 20
        }])

        prediction = model.predict(sample)[0]
        self.assertEqual(int(prediction), 0)


if __name__ == "__main__":
    unittest.main()
