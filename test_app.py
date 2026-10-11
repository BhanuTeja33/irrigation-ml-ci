import unittest

from app import app


class TestPredictionApplication(unittest.TestCase):

    def setUp(self):
        self.client = app.test_client()

    def test_health_endpoint(self):
        response = self.client.get("/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()["status"], "ok")

    def test_high_irrigation_need_prediction(self):
        response = self.client.post(
            "/predict",
            json={
                "soil_moisture": 15,
                "temperature": 40,
                "humidity": 30,
                "rainfall_forecast_mm": 0
            }
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.get_json()["prediction"],
            "IRRIGATE"
        )

    def test_low_irrigation_need_prediction(self):
        response = self.client.post(
            "/predict",
            json={
                "soil_moisture": 75,
                "temperature": 15,
                "humidity": 90,
                "rainfall_forecast_mm": 25
            }
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.get_json()["prediction"],
            "SKIP"
        )

    def test_missing_field_validation(self):
        response = self.client.post(
            "/predict",
            json={
                "soil_moisture": 40,
                "temperature": 30
            }
        )

        self.assertEqual(response.status_code, 400)
        self.assertIn(
            "missing_fields",
            response.get_json()
        )


if __name__ == "__main__":
    unittest.main()

