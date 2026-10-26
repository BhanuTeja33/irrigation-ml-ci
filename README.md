# Irrigation Need Prediction - MLOps CI/CD & Docker Pipeline

[![Irrigation ML CI-CD](https://github.com/BhanuTeja33/irrigation-ml-ci/actions/workflows/irrigation-ml-ci.yml/badge.svg)](https://github.com/BhanuTeja33/irrigation-ml-ci/actions)

An end-to-end Machine Learning Operations (MLOps) pipeline for real-time agricultural irrigation recommendation. The system ingests soil moisture and environmental weather telemetry to predict whether a farm plot requires immediate watering (`IRRIGATE`) or can conserve resources (`SKIP`).

---

## 📑 Practical Series Documentation

All lab practical manuals are compiled into Microsoft Word (`.docx`) format inside the [`Practical_Word_Documents/`](Practical_Word_Documents/) folder:

1. **Practical 2**: [PRACTICAL-2_Irrigation_ML_CI.docx](Practical_Word_Documents/PRACTICAL-2_Irrigation_ML_CI.docx) — Model training pipeline & automated ML tests in GitHub Actions.
2. **Practical 3**: [PRACTICAL-3_Irrigation_Quality_Gate.docx](Practical_Word_Documents/PRACTICAL-3_Irrigation_Quality_Gate.docx) — Automated ML quality gate enforcing accuracy thresholds.
3. **Practical 4**: [PRACTICAL-4_Preserving_Irrigation_Artifacts.docx](Practical_Word_Documents/PRACTICAL-4_Preserving_Irrigation_Artifacts.docx) — Model and metric artifact preservation.
4. **Practical 5**: [PRACTICAL-5_Continuous_Delivery_Irrigation_App.docx](Practical_Word_Documents/PRACTICAL-5_Continuous_Delivery_Irrigation_App.docx) — Continuous Delivery packaging and Flask prediction microservice.
5. **Practical 6**: [PRACTICAL-6_Dockerize_Irrigation_App.docx](Practical_Word_Documents/PRACTICAL-6_Dockerize_Irrigation_App.docx) — Containerization using Docker Desktop and local verification.
6. **Practical 7**: [PRACTICAL-7_Automate_Docker_Build_and_Test.docx](Practical_Word_Documents/PRACTICAL-7_Automate_Docker_Build_and_Test.docx) — Automated Docker build, container startup, health checking, and API testing in GitHub Actions CI.
7. **Practical 8**: [PRACTICAL-8_Publish_Docker_Image_to_GHCR.docx](Practical_Word_Documents/PRACTICAL-8_Publish_Docker_Image_to_GHCR.docx) — Manual publishing of tested Docker image to GitHub Container Registry (GHCR).
8. **Practical 9**: [PRACTICAL-9_Automate_Docker_Build_Test_Publish_GHCR.docx](Practical_Word_Documents/PRACTICAL-9_Automate_Docker_Build_Test_Publish_GHCR.docx) — Automated Docker build, container testing, and publishing to GHCR using GitHub Actions.

---

## 🏗️ Architecture & Pipeline Flow

```text
Code Change / Git Push to main
         │
         ▼
GitHub Actions CI/CD Runner (Ubuntu)
         │
         ├── 1. Build Docker Image (docker build -t irrigation-ml:ci .)
         │
         ├── 2. Run Test Container (-p 5000:5000)
         │
         ├── 3. Health Release Gate (GET http://localhost:5000/ with retry loop)
         │
         ├── 4. Prediction Smoke Test (curl POST /predict using test_payload.json)
         │
         ├── 5. Container Teardown (docker rm -f with if: always())
         │
         ├── 6. Authenticate to GHCR (using GITHUB_TOKEN)
         │
         ├── 7. Tag Image (:latest and :sha-<commit>)
         │
         ├── 8. Push Container Image to GHCR (ghcr.io/bhanuteja33/irrigation-ml)
         │
         ▼
Verified Container Published to GitHub Container Registry
```

---

## 🚀 Quickstart & Local Setup

### 1. Prerequisites
- Python 3.11+
- Docker Desktop

### 2. Environment Setup & Local Test
```bash
pip install -r requirements.txt
python train_irrigation_model.py
python irrigation_quality_gate.py
python -m unittest test_irrigation_ml.py
python -m unittest test_app.py
```

### 3. Docker Execution & Automated CI/CD
```bash
# Local container build & run
docker build -t irrigation-ml:1.0 .
docker run -d --name irrigation-ml-container -p 5000:5000 irrigation-ml:1.0
curl http://localhost:5000/

# Automated GitHub Actions Workflow
git add .
git commit -m "Automate Docker build, test, and publish to GHCR"
git push origin main
```
The automated workflow [`.github/workflows/docker-publish.yml`](.github/workflows/docker-publish.yml) builds, health-tests, and publishes `:latest` and `:sha-<commit>` directly to `ghcr.io/bhanuteja33/irrigation-ml`.
