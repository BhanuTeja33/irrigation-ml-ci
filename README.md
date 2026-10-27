# Irrigation Need Prediction - End-to-End MLOps Pipeline

[![Irrigation ML CI-CD](https://github.com/BhanuTeja33/irrigation-ml-ci/actions/workflows/docker-publish.yml/badge.svg)](https://github.com/BhanuTeja33/irrigation-ml-ci/actions)
[![Live Service on Render](https://img.shields.io/badge/Render-Live%20Service-success)](https://irrigation-ml-service-5pt9.onrender.com/)
[![GHCR Package](https://img.shields.io/badge/GHCR-irrigation--ml-blue)](https://github.com/users/BhanuTeja33/packages/container/package/irrigation-ml)

An end-to-end Machine Learning Operations (MLOps) pipeline for real-time agricultural irrigation recommendation. The system ingests soil moisture and environmental weather telemetry to predict whether a farm plot requires immediate watering (`IRRIGATE`) or can conserve resources (`SKIP`).

---

## 📑 Complete Lab Series Documentation (Practicals 2 – 10)

All laboratory practical manuals are fully documented and compiled into Microsoft Word (`.docx`) format inside the [`Practical_Word_Documents/`](Practical_Word_Documents/) folder:

| Practical | Manual Document | Description & Highlights | Status |
|:---:|---|---|:---:|
| **P2** | [PRACTICAL-2_Irrigation_ML_CI.docx](Practical_Word_Documents/PRACTICAL-2_Irrigation_ML_CI.docx) | Automated ML model training pipeline, feature scaling, and unit testing in GitHub Actions CI. | ✅ Complete |
| **P3** | [PRACTICAL-3_Irrigation_Quality_Gate.docx](Practical_Word_Documents/PRACTICAL-3_Irrigation_Quality_Gate.docx) | Machine Learning Quality Gate enforcing a minimum accuracy threshold of 90.0% before release. | ✅ Complete |
| **P4** | [PRACTICAL-4_Preserving_Irrigation_Artifacts.docx](Practical_Word_Documents/PRACTICAL-4_Preserving_Irrigation_Artifacts.docx) | Model artifact retention (`irrigation_model.pkl`, `metrics.json`) using `actions/upload-artifact@v4`. | ✅ Complete |
| **P5** | [PRACTICAL-5_Continuous_Delivery_Irrigation_App.docx](Practical_Word_Documents/PRACTICAL-5_Continuous_Delivery_Irrigation_App.docx) | Continuous Delivery packaging and Flask prediction microservice (`app.py`) with health & inference endpoints. | ✅ Complete |
| **P6** | [PRACTICAL-6_Dockerize_Irrigation_App.docx](Practical_Word_Documents/PRACTICAL-6_Dockerize_Irrigation_App.docx) | Application containerization using `python:3.11-slim`, Docker build, port forwarding (5000:5000), and local verification. | ✅ Complete |
| **P7** | [PRACTICAL-7_Automate_Docker_Build_and_Test.docx](Practical_Word_Documents/PRACTICAL-7_Automate_Docker_Build_and_Test.docx) | Automated Docker container build, startup, readiness wait, and endpoint smoke testing inside GitHub Actions. | ✅ Complete |
| **P8** | [PRACTICAL-8_Publish_Docker_Image_to_GHCR.docx](Practical_Word_Documents/PRACTICAL-8_Publish_Docker_Image_to_GHCR.docx) | Manual container publication to GitHub Container Registry (`ghcr.io/bhanuteja33/irrigation-ml:v1` and `:latest`). | ✅ Complete |
| **P9** | [PRACTICAL-9_Irrigation_ML_GHCR_Final.docx](Practical_Word_Documents/PRACTICAL-9_Irrigation_ML_GHCR_Final.docx) | **Automated CI/CD Pipeline:** Complete workflow automating training, testing, Docker build, and GHCR publishing on every push to `main`. *(Includes real terminal & GitHub Actions execution screenshots)* | ✅ Complete |
| **P10** | [PRACTICAL-10_Deploy_GHCR_Image_to_Render_Final.docx](Practical_Word_Documents/PRACTICAL-10_Deploy_GHCR_Image_to_Render_Final.docx) | **Production Cloud Deployment:** Deployed prebuilt GHCR container image to a public **Render Web Service**, configured port mapping (`PORT=5000`), and verified live HTTPS endpoints. *(Includes live Render deployment and API testing screenshots)* | ✅ Complete |

---

## 🏗️ End-to-End MLOps Architecture

```text
  Developer Push to 'main'
            │
            ▼
┌────────────────────────────────────────────────────────────────────────┐
│               GitHub Actions CI/CD (Practical 9)                       │
│  1. Setup Python 3.11 & install dependencies                           │
│  2. Run training pipeline -> Generate irrigation_model.pkl             │
│  3. Evaluate Quality Gate (Accuracy > 90%)                             │
│  4. Run automated ML & Flask API unit tests                            │
│  5. Build Docker Image (python:3.11-slim)                              │
│  6. In-runner container test (curl http://localhost:5000/ & /predict)  │
│  7. Authenticate using GITHUB_TOKEN (packages: write)                  │
│  8. Tag & Push to GitHub Container Registry                            │
└──────────────────────────────────┬─────────────────────────────────────┘
                                   │
                                   ▼
┌────────────────────────────────────────────────────────────────────────┐
│            GitHub Container Registry (GHCR)                            │
│  - Image: ghcr.io/bhanuteja33/irrigation-ml                            │
│  - Tags: :latest, :f5c85dd... (immutable commit SHA)                   │
└──────────────────────────────────┬─────────────────────────────────────┘
                                   │
                                   │ Image pull over HTTPS
                                   ▼
┌────────────────────────────────────────────────────────────────────────┐
│            Render Cloud Web Service (Practical 10)                     │
│  - Image-Backed Web Service (bypasses buildpack source build)          │
│  - Instance Tier: Free (0.1 CPU, 512 MB RAM, Singapore region)         │
│  - Ingress Routing: PORT = 5000, Host: 0.0.0.0                         │
│  - Health Check: / (HTTP 200 OK)                                       │
│  - Public HTTPS URL: https://irrigation-ml-service-5pt9.onrender.com   │
└──────────────────────────────────┬─────────────────────────────────────┘
                                   │
                                   ▼
┌────────────────────────────────────────────────────────────────────────┐
│                      Live Production Verification                      │
│  - GET  /        -> {"service":"irrigation-need-prediction","ok"}      │
│  - POST /predict -> {"prediction":"IRRIGATE","prediction_code":1}      │
└────────────────────────────────────────────────────────────────────────┘
```

---

## 🌐 Live Production Service Details (Practical 10)

- **Production Cloud Host:** [Render.com](https://render.com)
- **Primary Public Endpoint:** [`https://irrigation-ml-service-5pt9.onrender.com`](https://irrigation-ml-service-5pt9.onrender.com)
- **Deployment Type:** Image-Backed Web Service (Pulled directly from GHCR)
- **Status:** `Deploy succeeded | Live` (Deployment duration: 40.1s)
- **Container Port:** `5000` (`PORT=5000`)
- **Health Check Path:** `/`

### Live API Verification

#### 1. Root Health Check (GET)
```powershell
curl https://irrigation-ml-service-5pt9.onrender.com/
```
**Response:**
```json
{
  "service": "irrigation-need-prediction",
  "status": "ok"
}
```

#### 2. Machine Learning Inference (POST /predict)
```powershell
Invoke-RestMethod -Uri "https://irrigation-ml-service-5pt9.onrender.com/predict" `
  -Method Post `
  -Body '{"soil_moisture":15,"temperature":40,"humidity":30,"rainfall_forecast_mm":0}' `
  -ContentType "application/json"
```
**Response:**
```text
prediction  prediction_code
----------  ---------------
IRRIGATE    1
```

---

## 💻 Local Setup & Quickstart

### 1. Prerequisites
- Python 3.11+
- Docker Desktop (running)
- Git

### 2. Local Training & Quality Gate
```bash
pip install -r requirements.txt
python train_irrigation_model.py
python irrigation_quality_gate.py
pytest test_irrigation_ml.py -v
pytest test_app.py -v
```

### 3. Local Container Build & Verification
```bash
docker build -t irrigation-ml:1.0 .
docker run -d --name irrigation-test -p 5000:5000 irrigation-ml:1.0
curl http://localhost:5000/
curl -X POST http://localhost:5000/predict -H "Content-Type: application/json" -d @test_payload.json
docker rm -f irrigation-test
```

---

## 👤 Author Information
- **Student Name:** Bhanu Teja Velpuri
- **GitHub Username:** [BhanuTeja33](https://github.com/BhanuTeja33)
- **Repository:** [irrigation-ml-ci](https://github.com/BhanuTeja33/irrigation-ml-ci)
- **GHCR Package:** [ghcr.io/bhanuteja33/irrigation-ml](https://github.com/users/BhanuTeja33/packages/container/package/irrigation-ml)
- **Date:** October 2026
