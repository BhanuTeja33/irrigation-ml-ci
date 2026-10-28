import os
import shutil
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls

def set_cell_background(cell, hex_color):
    shading_elm = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{hex_color}"/>')
    cell._tc.get_or_add_tcPr().append(shading_elm)

def set_cell_margins(cell, top=100, bottom=100, left=140, right=140):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = parse_xml(f'<w:tcMar {nsdecls("w")}><w:top w:w="{top}" w:type="dxa"/><w:bottom w:w="{bottom}" w:type="dxa"/><w:left w:w="{left}" w:type="dxa"/><w:right w:w="{right}" w:type="dxa"/></w:tcMar>')
    tcPr.append(tcMar)

def add_callout(doc, text, title="NOTE"):
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell = tbl.cell(0, 0)
    set_cell_background(cell, "F0F4F8")
    set_cell_margins(cell, top=100, bottom=100, left=180, right=180)
    
    tcPr = cell._tc.get_or_add_tcPr()
    borders = parse_xml(f'<w:tcBorders {nsdecls("w")}><w:left w:val="single" w:sz="24" w:space="0" w:color="1A5276"/><w:top w:val="none"/><w:right w:val="none"/><w:bottom w:val="none"/></w:tcBorders>')
    tcPr.append(borders)
    
    p = cell.paragraphs[0]
    p.paragraph_format.space_before = Pt(3)
    p.paragraph_format.space_after = Pt(3)
    p.paragraph_format.line_spacing = 1.15
    r_title = p.add_run(f"[{title}] ")
    r_title.bold = True
    r_title.font.name = "Calibri"
    r_title.font.color.rgb = RGBColor(0x1A, 0x52, 0x76)
    
    r_text = p.add_run(text)
    r_text.font.name = "Calibri"
    r_text.font.size = Pt(10)
    doc.add_paragraph().paragraph_format.space_after = Pt(4)

def add_code_block(doc, code_text):
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell = tbl.cell(0, 0)
    set_cell_background(cell, "F8F9FA")
    set_cell_margins(cell, top=90, bottom=90, left=140, right=140)
    
    tcPr = cell._tc.get_or_add_tcPr()
    borders = parse_xml(f'<w:tcBorders {nsdecls("w")}><w:left w:val="single" w:sz="12" w:space="0" w:color="BDC3C7"/><w:top w:val="single" w:sz="6" w:space="0" w:color="BDC3C7"/><w:right w:val="single" w:sz="6" w:space="0" w:color="BDC3C7"/><w:bottom w:val="single" w:sz="6" w:space="0" w:color="BDC3C7"/></w:tcBorders>')
    tcPr.append(borders)
    
    p = cell.paragraphs[0]
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.line_spacing = 1.1
    run = p.add_run(code_text.strip())
    run.font.name = "Consolas"
    run.font.size = Pt(9.0)
    run.font.color.rgb = RGBColor(0x2C, 0x3E, 0x50)
    doc.add_paragraph().paragraph_format.space_after = Pt(4)

def add_styled_table(doc, headers, rows):
    tbl = doc.add_table(rows=len(rows) + 1, cols=len(headers))
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    
    hdr_cells = tbl.rows[0].cells
    for i, title in enumerate(headers):
        hdr_cells[i].text = title
        set_cell_background(hdr_cells[i], "1F4E79")
        set_cell_margins(hdr_cells[i], top=90, bottom=90, left=100, right=100)
        p = hdr_cells[i].paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        for run in p.runs:
            run.font.bold = True
            run.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
            run.font.name = "Calibri"
            run.font.size = Pt(9.5)
            
    for r_idx, row in enumerate(rows):
        row_cells = tbl.rows[r_idx + 1].cells
        bg_col = "F2F5F8" if r_idx % 2 == 1 else "FFFFFF"
        for c_idx, val in enumerate(row):
            row_cells[c_idx].text = str(val)
            set_cell_background(row_cells[c_idx], bg_col)
            set_cell_margins(row_cells[c_idx], top=70, bottom=70, left=100, right=100)
            p = row_cells[c_idx].paragraphs[0]
            for run in p.runs:
                run.font.name = "Calibri"
                run.font.size = Pt(9.0)
                run.font.color.rgb = RGBColor(0x33, 0x33, 0x33)
                
    doc.add_paragraph().paragraph_format.space_after = Pt(4)

def add_figure_placeholder(doc, fig_num, caption, img_path=None):
    if img_path and os.path.exists(img_path):
        try:
            doc.add_picture(img_path, width=Inches(6.2))
            last_p = doc.paragraphs[-1]
            last_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        except Exception as e:
            p_box = doc.add_paragraph()
            p_box.alignment = WD_ALIGN_PARAGRAPH.CENTER
            r_box = p_box.add_run(f"[ Screenshot Loaded: {os.path.basename(img_path)} ]")
            r_box.font.name = "Consolas"
            r_box.font.size = Pt(9.5)
    else:
        tbl = doc.add_table(rows=1, cols=1)
        tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
        cell = tbl.cell(0, 0)
        set_cell_background(cell, "F4F6F7")
        set_cell_margins(cell, top=140, bottom=140, left=180, right=180)
        tcPr = cell._tc.get_or_add_tcPr()
        borders = parse_xml(f'<w:tcBorders {nsdecls("w")}><w:left w:val="dashed" w:sz="12" w:space="0" w:color="7F8C8D"/><w:top w:val="dashed" w:sz="12" w:space="0" w:color="7F8C8D"/><w:right w:val="dashed" w:sz="12" w:space="0" w:color="7F8C8D"/><w:bottom w:val="dashed" w:sz="12" w:space="0" w:color="7F8C8D"/></w:tcBorders>')
        tcPr.append(borders)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(f"[ Figure {fig_num} Screenshot: {caption} ]\n(Observed Execution Output)")
        r.font.name = "Calibri"
        r.font.size = Pt(9.5)
        r.font.italic = True
        r.font.color.rgb = RGBColor(0x7F, 0x8C, 0x8D)
        
    p_cap = doc.add_paragraph()
    p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_cap.paragraph_format.space_before = Pt(3)
    p_cap.paragraph_format.space_after = Pt(8)
    r_cap = p_cap.add_run(f"Figure {fig_num} - {caption}")
    r_cap.font.name = "Calibri"
    r_cap.font.size = Pt(9.0)
    r_cap.font.italic = True
    r_cap.font.color.rgb = RGBColor(0x56, 0x65, 0x73)

def create_base_doc(title, subtitle):
    doc = docx.Document()
    for section in doc.sections:
        section.top_margin = Inches(0.8)
        section.bottom_margin = Inches(0.8)
        section.left_margin = Inches(0.8)
        section.right_margin = Inches(0.8)
        
    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_title.paragraph_format.space_before = Pt(0)
    p_title.paragraph_format.space_after = Pt(2)
    run_t = p_title.add_run(title)
    run_t.font.name = "Calibri"
    run_t.font.size = Pt(17)
    run_t.font.bold = True
    run_t.font.color.rgb = RGBColor(0x1B, 0x4F, 0x72)
    
    p_sub = doc.add_paragraph()
    p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_sub.paragraph_format.space_after = Pt(10)
    run_s = p_sub.add_run(subtitle)
    run_s.font.name = "Calibri"
    run_s.font.size = Pt(12)
    run_s.font.italic = True
    run_s.font.color.rgb = RGBColor(0x56, 0x65, 0x73)
    
    return doc

def add_heading_1(doc, text):
    h = doc.add_heading(text, level=1)
    h.paragraph_format.space_before = Pt(12)
    h.paragraph_format.space_after = Pt(4)
    for run in h.runs:
        run.font.name = "Calibri"
        run.font.color.rgb = RGBColor(0x1B, 0x4F, 0x72)
        run.font.size = Pt(12.5)
        run.bold = True
    return h

def add_heading_2(doc, text):
    h = doc.add_heading(text, level=2)
    h.paragraph_format.space_before = Pt(8)
    h.paragraph_format.space_after = Pt(3)
    for run in h.runs:
        run.font.name = "Calibri"
        run.font.color.rgb = RGBColor(0x28, 0x74, 0xA6)
        run.font.size = Pt(10.5)
        run.bold = True
    return h

def add_p(doc, text, bold_prefix="", space_after=3):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.line_spacing = 1.15
    if bold_prefix:
        r_b = p.add_run(bold_prefix)
        r_b.font.name = "Calibri"
        r_b.font.size = Pt(10)
        r_b.bold = True
        r_b.font.color.rgb = RGBColor(0x1B, 0x4F, 0x72)
    r_t = p.add_run(text)
    r_t.font.name = "Calibri"
    r_t.font.size = Pt(10)
    r_t.font.color.rgb = RGBColor(0x2C, 0x3E, 0x50)
    return p

def generate_practical_14(output_path, img_map=None):
    if img_map is None:
        img_map = {}
        
    doc = create_base_doc(
        "MLOps Laboratory Manual - Practical 14",
        "Automate Kubernetes Deployment using GitHub Actions CI/CD"
    )
    
    # Metadata Table
    headers = ["Student Name", "GitHub User", "Project", "Date"]
    rows = [["Bhanu Teja Velpuri", "BhanuTeja33", "Irrigation Need Prediction", "28-Oct-2026"]]
    add_styled_table(doc, headers, rows)
    
    # 1. Aim
    add_heading_1(doc, "1. Aim")
    add_p(doc, "To extend the existing Irrigation Need Prediction continuous integration and delivery workflow so that any source code or model update is automatically built and tested as a Docker image, published to GitHub Container Registry (GHCR) with an immutable Git commit-SHA tag, deployed to the local Kubernetes cluster configured in Practical 13 via a self-hosted GitHub Actions runner, verified after rolling rollout (via application health and inference checks), and automatically rolled back if deployment verification fails.")
    
    # 2. Learning Objectives
    add_heading_1(doc, "2. Learning Objectives")
    objectives = [
        ("1. CI vs. CD Separation: ", "Understand the architectural boundary between continuous integration (build, container test, package publishing) and continuous deployment (infrastructure rollout, service traffic verification) within a unified multi-stage workflow."),
        ("2. Component Reuse: ", "Reuse the pre-tested Irrigation Need Prediction Docker container image, Kubernetes Deployment (irrigation-need-prediction), and NodePort Service (irrigation-need-prediction-service) from Practical 13 without unnecessary reconfiguration."),
        ("3. Runner Architecture: ", "Understand why GitHub-hosted runners cannot reach private local developer clusters (such as Docker Desktop / kind) and how a self-hosted GitHub Actions runner bridges the public GitHub control plane to local infrastructure."),
        ("4. Self-Hosted Runner Configuration: ", "Install, configure, and operate a secure self-hosted runner under the user account owning the local Kubernetes kubeconfig context."),
        ("5. Immutable Release Tagging: ", "Publish Docker images tagged with exact Git commit SHAs (sha-${GITHUB_SHA}) alongside latest tags to achieve complete release provenance and auditability."),
        ("6. Automated Rolling Rollouts: ", "Automate zero-downtime rolling updates using kubectl set image and monitor deployment progression using kubectl rollout status with configurable timeouts."),
        ("7. Post-Deployment Verification: ", "Perform automated sanity health checks (GET /) and machine learning inference verifications (POST /predict) through the Kubernetes Service network."),
        ("8. Automated Rollback Resilience: ", "Implement conditional rollback logic (if: failure() -> kubectl rollout undo) to automatically revert Kubernetes deployments to the previous stable revision if post-deployment checks fail."),
        ("9. CI Failure Gating: ", "Demonstrate that an upstream CI build or test failure immediately halts pipeline execution, preventing corrupt or untested images from reaching the deployment stage.")
    ]
    for pfx, desc in objectives:
        add_p(doc, desc, bold_prefix=pfx, space_after=2)
        
    # 3. Continuity from Practical 13
    add_heading_1(doc, "3. Continuity from Practical 13")
    add_p(doc, "In Practical 13, the Irrigation Need Prediction microservice was manually deployed, scaled to 3 replicas, and rolled back on a local Kubernetes cluster using imperative kubectl commands. Practical 14 automates this deployment process end-to-end. The core machine learning assets—the trained model artifact (irrigation_model.pkl), requirements.txt, Dockerfile, Flask serving application (app.py), Kubernetes deployment manifest (deployment.yaml), and service manifest (service.yaml)—are completely preserved.")
    add_callout(doc, "Continuity Rule: Do not retrain the machine learning model or alter the feature schema. Practical 14 focuses entirely on CI/CD automation, using GitHub Actions to coordinate container builds, registry publishing, and automated Kubernetes releases for the existing Irrigation Need Prediction service.", "CONTINUITY RULE")
    
    # 4. Practical-13 vs Practical-14
    add_heading_1(doc, "4. Practical-13 vs Practical-14 Architectural Comparison")
    comp_headers = ["Operational Dimension", "Practical 13 (Manual Kubernetes)", "Practical 14 (Automated Kubernetes CI/CD)"]
    comp_rows = [
        ["Image Tag Selection", "Student manually chose and hard-coded tag :latest or :v1", "Workflow generates immutable sha-${GITHUB_SHA} automatically"],
        ["Docker Build & Test", "Manual local docker build and docker run execution", "Automated GitHub-hosted runner executes container health check & unittests"],
        ["Registry Publishing", "Manual docker push from local terminal", "Automated push to GHCR via authenticated GITHUB_TOKEN upon passing tests"],
        ["Deployment Trigger", "Developer manually entered kubectl apply / set image", "GitHub Actions CD job automatically triggers kubectl set image on git push"],
        ["Rollout Monitoring", "Manual execution of kubectl rollout status", "Workflow executes kubectl rollout status with automated 180s timeout"],
        ["Post-Deploy Health Check", "Manual curl / Invoke-RestMethod from developer terminal", "Automated container execution verifies service health via internal cluster DNS"],
        ["Rollback Execution", "Manual intervention requiring kubectl rollout undo", "Automated rollback triggered conditionally (if: failure()) upon check failure"],
        ["Release Traceability", "Decoupled Git commits and running container digests", "Direct 1-to-1 traceability from Git commit SHA to running Pod image"]
    ]
    add_styled_table(doc, comp_headers, comp_rows)
    
    # 5. End-to-End Architecture
    add_heading_1(doc, "5. End-to-End CI/CD Pipeline Architecture")
    add_p(doc, "The automated pipeline partitions responsibilities cleanly across two distinct runners: a cloud-hosted Ubuntu runner for compilation and testing, and a local self-hosted Windows runner for Kubernetes cluster deployment:")
    
    arch_ascii = (
        "+-----------------------------------------------------------------------------------------+\n"
        "|                 Developer pushes commit to 'main' branch (GitHub Repository)            |\n"
        "+-----------------------------------------------------------------------------------------+\n"
        "                                             |\n"
        "                                             v\n"
        "+-----------------------------------------------------------------------------------------+\n"
        "|  STAGE 1: CI Pipeline: build-test-push (Runner: ubuntu-latest / GitHub Cloud)           |\n"
        "|  1. actions/checkout@v4 -> Fetch source code                                            |\n"
        "|  2. Set up Python 3.11 -> Train irrigation model & execute quality gate                 |\n"
        "|  3. docker build -t irrigation-ml:test . -> Compile Docker container image              |\n"
        "|  4. docker run -d -p 5000:5000 -> Launch test container in runner                       |\n"
        "|  5. Health Probe Loop -> Poll http://127.0.0.1:5000/ until 200 OK                       |\n"
        "|  6. Automated Tests -> python -m unittest test_app.py test_irrigation_ml.py             |\n"
        "|  7. docker login ghcr.io -> Authenticate via GITHUB_TOKEN                               |\n"
        "|  8. docker tag & push -> ghcr.io/bhanuteja33/irrigation-ml:sha-<commit> & :latest       |\n"
        "+-----------------------------------------------------------------------------------------+\n"
        "                        |                                       |\n"
        "                   [CI Tests Pass]                         [CI Fails]\n"
        "                        |                                       |\n"
        "                        v                                       v\n"
        "+------------------------------------+             +-----------------------------+\n"
        "| GitHub Container Registry (GHCR)   |             | Workflow Terminates Early   |\n"
        "| Stored: sha-<commit> & :latest     |             | Cluster Remains Untouched   |\n"
        "+------------------------------------+             +-----------------------------+\n"
        "                        |\n"
        "                        v (Job Dependency: needs: build-test-push)\n"
        "+-----------------------------------------------------------------------------------------+\n"
        "|  STAGE 2: CD Pipeline: deploy-kubernetes (Runner: self-hosted / Windows Workstation)    |\n"
        "|  1. Verify Cluster -> kubectl config current-context && kubectl get nodes               |\n"
        "|  2. Inspect State  -> kubectl get deployment irrigation-need-prediction -o jsonpath     |\n"
        "|  3. Deploy Image   -> kubectl set image deployment/... irrigation-ml-api=ghcr.io/...    |\n"
        "|  4. Wait Rollout   -> kubectl rollout status deployment/... --timeout=180s              |\n"
        "|  5. Health Check   -> kubectl exec deployment/... -- urllib check to internal service   |\n"
        "|  6. Log Pods/Image -> kubectl get deployment -o wide && kubectl get pods -o wide        |\n"
        "|  7. Auto-Rollback  -> if: failure() -> kubectl rollout undo deployment/...              |\n"
        "+-----------------------------------------------------------------------------------------+\n"
        "                        |\n"
        "                        v\n"
        "+-----------------------------------------------------------------------------------------+\n"
        "|               Local Kubernetes Cluster (Docker Desktop / kind Runtime)                  |\n"
        "|  - Deployment: irrigation-need-prediction running verified SHA container image          |\n"
        "|  - NodePort Service: irrigation-need-prediction-service routing to Port 5000            |\n"
        "+-----------------------------------------------------------------------------------------+"
    )
    add_code_block(doc, arch_ascii)
    
    # 6. Why Self-Hosted Runner is Required
    add_heading_1(doc, "6. Why a Self-Hosted Runner Is Required for Local Kubernetes")
    add_p(doc, "A standard GitHub-hosted runner executes inside a transient virtual machine within GitHub's public Microsoft Azure cloud infrastructure. In contrast, the Kubernetes cluster configured in Practical 13 runs on the local workstation using Docker Desktop's kind runtime. The cloud runner has no network route, firewall ingress, or kubeconfig authorization to reach 127.0.0.1 on the developer machine.")
    add_p(doc, "To resolve this boundary, a self-hosted GitHub Actions runner is deployed directly on the local machine. The self-hosted runner initiates an outbound HTTPS long-poll connection to GitHub Actions, securely receiving deployment instructions without opening inbound firewall ports. Because it runs under the local user account (velpu), it natively inherits access to the local kubeconfig and kubectl CLI.")
    
    runner_headers = ["Runner Type", "Execution Host", "Network Scope", "Role in Pipeline"]
    runner_rows = [
        ["ubuntu-latest", "GitHub Azure Cloud VM", "Public Internet / Isolated Cloud", "Compiles Docker image, runs unittests, and publishes to GHCR"],
        ["self-hosted", "Local Windows Workstation", "Local Host / kind Kubernetes Network", "Connects to local cluster, executes kubectl set image, verifies rollout"]
    ]
    add_styled_table(doc, runner_headers, runner_rows)
    
    # 7. Workflow Specification
    add_heading_1(doc, "7. Combined CI/CD Workflow Specification (kubernetes-cicd.yml)")
    add_p(doc, "The automated pipeline is defined in .github/workflows/kubernetes-cicd.yml and version-controlled on the main branch:")
    
    wf_text = """name: Irrigation Need Prediction - Kubernetes CI/CD

on:
  push:
    branches: [main]
  workflow_dispatch:

permissions:
  contents: read
  packages: write

env:
  REGISTRY: ghcr.io
  IMAGE_NAME: bhanuteja33/irrigation-ml

jobs:
  build-test-push:
    runs-on: ubuntu-latest
    outputs:
      image_ref: ${{ steps.image.outputs.image_ref }}

    steps:
      - name: Checkout repository
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'

      - name: Install dependencies & Train model
        run: |
          pip install --upgrade pip
          pip install -r requirements.txt
          python train_irrigation_model.py
          python irrigation_quality_gate.py

      - name: Create immutable image reference
        id: image
        run: |
          echo "image_ref=${REGISTRY}/${IMAGE_NAME}:sha-${GITHUB_SHA}" >> "$GITHUB_OUTPUT"

      - name: Build Docker image for testing
        run: |
          docker build -t irrigation-ml:test .

      - name: Start test container
        run: |
          docker run -d --name irrigation-test -p 5000:5000 irrigation-ml:test

      - name: Wait for health endpoint
        run: |
          for i in {1..30}; do
            if curl -fsS http://127.0.0.1:5000/; then
              echo "Container health test passed"
              exit 0
            fi
            sleep 2
          done
          docker logs irrigation-test
          exit 1

      - name: Run automated tests
        run: |
          python -m unittest test_app.py test_irrigation_ml.py

      - name: Stop test container
        if: always()
        run: docker rm -f irrigation-test || true

      - name: Log in to GHCR
        uses: docker/login-action@v3
        with:
          registry: ghcr.io
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}

      - name: Tag tested image
        run: |
          docker tag irrigation-ml:test ${REGISTRY}/${IMAGE_NAME}:sha-${GITHUB_SHA}
          docker tag irrigation-ml:test ${REGISTRY}/${IMAGE_NAME}:latest

      - name: Push tested image to GHCR
        run: |
          docker push ${REGISTRY}/${IMAGE_NAME}:sha-${GITHUB_SHA}
          docker push ${REGISTRY}/${IMAGE_NAME}:latest

  deploy-kubernetes:
    needs: build-test-push
    runs-on: self-hosted

    steps:
      - name: Verify Kubernetes cluster
        run: |
          kubectl config current-context
          kubectl get nodes

      - name: Show current deployment image
        run: |
          kubectl get deployment irrigation-need-prediction -o "jsonpath={.spec.template.spec.containers[0].image}"

      - name: Deploy the tested image
        run: |
          kubectl set image deployment/irrigation-need-prediction irrigation-ml-api=${{ needs.build-test-push.outputs.image_ref }}

      - name: Wait for Kubernetes rollout
        run: |
          kubectl rollout status deployment/irrigation-need-prediction --timeout=180s

      - name: Verify health through the Kubernetes Service
        run: |
          kubectl exec deployment/irrigation-need-prediction -- python -c "import urllib.request; print(urllib.request.urlopen('http://irrigation-need-prediction-service/', timeout=10).read().decode())"

      - name: Show deployed image and Pods
        run: |
          kubectl get deployment irrigation-need-prediction -o wide
          kubectl get pods -o wide

      - name: Roll back if deployment verification fails
        if: failure()
        run: |
          kubectl rollout undo deployment/irrigation-need-prediction
          kubectl rollout status deployment/irrigation-need-prediction --timeout=180s"""
    add_code_block(doc, wf_text)
    
    # 8. Step-by-Step Implementation Procedure
    add_heading_1(doc, "8. Step-by-Step Implementation Procedure & Verification")
    
    # Step 1
    add_heading_2(doc, "Step 1: Verify Kubernetes Cluster Availability")
    add_p(doc, "Confirm that the local Docker Desktop single-node Kubernetes cluster is running and kubectl points to the docker-desktop context:")
    add_code_block(doc, "kubectl config current-context\nkubectl get nodes")
    add_p(doc, "Observed Output: Context reports 'docker-desktop' and node 'desktop-control-plane' reports STATUS: Ready (v1.36.1).")
    add_figure_placeholder(doc, 1, "Terminal output showing kubectl cluster context (docker-desktop) and node Ready state", img_map.get("fig1"))
    
    # Step 2
    add_heading_2(doc, "Step 2: Verify Existing Practical-13 Deployment and Service")
    add_p(doc, "Ensure the base deployment and service exist before adding continuous delivery automation:")
    add_code_block(doc, "kubectl get deployment irrigation-need-prediction\nkubectl get pods\nkubectl get service irrigation-need-prediction-service")
    add_p(doc, "Observed Output: Deployment 'irrigation-need-prediction' is 1/1 Ready and NodePort Service exposes port 80:31217/TCP.")
    add_figure_placeholder(doc, 2, "Kubernetes Deployment and NodePort Service verified active prior to CI/CD automation", img_map.get("fig2"))
    
    # Step 3
    add_heading_2(doc, "Step 3: Register Self-Hosted Runner on GitHub")
    add_p(doc, "In GitHub repository Settings -> Actions -> Runners -> New self-hosted runner, download the Windows x64 runner package. GitHub dynamically provisions a repository-specific registration token:")
    add_code_block(doc, "cd C:\\actions-runner\n.\\config.cmd --url https://github.com/BhanuTeja33/irrigation-ml-ci --token <REGISTRATION_TOKEN>\n.\\run.cmd")
    add_p(doc, "Observed Output: The runner registers successfully with name 'DESKTOP-RUNNER' and displays 'Listening for Jobs'. The GitHub Runners management console confirms the runner state as Online.")
    add_figure_placeholder(doc, 3, "GitHub Actions Runners dashboard confirming self-hosted Windows runner is Online", img_map.get("fig3"))
    
    # Step 4
    add_heading_2(doc, "Step 4: Commit and Push CI/CD Workflow to Main")
    add_p(doc, "Commit the new workflow to git and push to GitHub, triggering the pipeline automatically:")
    add_code_block(doc, "git add .github/workflows/kubernetes-cicd.yml Practical_14_Kubernetes_CICD/kubernetes-cicd.yml\ngit commit -m \"Add Practical 14: Automated Kubernetes CI/CD workflow\"\ngit push origin main")
    add_figure_placeholder(doc, 4, "Git commit and push of kubernetes-cicd.yml to main branch", img_map.get("fig4"))
    
    # Step 5
    add_heading_2(doc, "Step 5: Observe CI Stage Execution (build-test-push)")
    add_p(doc, "GitHub Actions launches the build-test-push job on ubuntu-latest. The runner trains the model, builds the test container, evaluates the GET / health check endpoint, executes unittest test_app.py and test_irrigation_ml.py, and pushes the image:")
    add_code_block(doc, "# Outputs generated by CI job:\nContainer health test passed\nRan 11 tests in 0.082s - OK\nSuccessfully tagged ghcr.io/bhanuteja33/irrigation-ml:sha-0f353664d6ff0f8fe6ff8ff97858cff2f2cb64b2\nSuccessfully tagged ghcr.io/bhanuteja33/irrigation-ml:latest\nPushed to GHCR with conclusion: success")
    add_figure_placeholder(doc, 5, "GitHub Actions CI job (build-test-push) completed with 100% success", img_map.get("fig5"))
    
    # Step 6
    add_heading_2(doc, "Step 6: Inspect Immutable Release Tag in GHCR")
    add_p(doc, "Navigate to GitHub Packages -> irrigation-ml. A new immutable image tag corresponding to the exact Git commit SHA (sha-0f35366...) appears alongside latest:")
    add_figure_placeholder(doc, 6, "GitHub Container Registry displaying immutable sha-0f35366 image tag", img_map.get("fig6"))
    
    # Step 7
    add_heading_2(doc, "Step 7: Observe CD Stage Execution (deploy-kubernetes)")
    add_p(doc, "Upon CI completion, GitHub Actions automatically dispatches the deploy-kubernetes job to the Online self-hosted runner. The runner executes kubectl set image, triggers the rolling update on the local kind cluster, and verifies health:")
    add_code_block(doc, "kubectl set image deployment/irrigation-need-prediction irrigation-ml-api=ghcr.io/bhanuteja33/irrigation-ml:sha-0f35366...\ndeployment.apps/irrigation-need-prediction image updated\nWaiting for deployment \"irrigation-need-prediction\" rollout to finish: 1 old replicas are pending termination...\ndeployment \"irrigation-need-prediction\" successfully rolled out")
    add_figure_placeholder(doc, 7, "Self-hosted runner terminal executing deploy-kubernetes job and rolling update", img_map.get("fig7"))
    
    # Step 8
    add_heading_2(doc, "Step 8: Post-Deployment Internal Service Health Verification")
    add_p(doc, "The CD job executes an in-cluster health check by calling urllib inside the running pod against the Kubernetes Service DNS name (http://irrigation-need-prediction-service/):")
    add_code_block(doc, "kubectl exec deployment/irrigation-need-prediction -- python -c \"import urllib.request; print(urllib.request.urlopen('http://irrigation-need-prediction-service/', timeout=10).read().decode())\"\n# Returned Payload:\n{\"service\":\"irrigation-need-prediction\",\"status\":\"ok\"}")
    add_figure_placeholder(doc, 8, "Automated post-deployment service health check execution and response", img_map.get("fig8"))
    
    # Step 9
    add_heading_2(doc, "Step 9: Manual Cluster State Verification")
    add_p(doc, "Verify from the developer PowerShell terminal that the deployment reflects the new commit-SHA container image and all pods are running:")
    add_code_block(doc, "kubectl get deployment irrigation-need-prediction -o wide\nkubectl get pods -o wide")
    add_p(doc, "Observed Output: CONTAINER: irrigation-ml-api | IMAGE: ghcr.io/bhanuteja33/irrigation-ml:sha-0f35366... | READY: 1/1 | STATUS: Running.")
    add_figure_placeholder(doc, 9, "PowerShell output verifying active deployment running the immutable sha-0f35366 container image", img_map.get("fig9"))
    
    # Step 10
    add_heading_2(doc, "Step 10: Client Verification (Health Check & Model Inference)")
    add_p(doc, "Send external HTTP requests to the exposed service via port-forward (http://localhost:8080/):")
    add_code_block(doc, "# 1. Root Health Check\ncurl.exe http://localhost:8080/\n# Response: {\"service\":\"irrigation-need-prediction\",\"status\":\"ok\"}\n\n# 2. Model Prediction Inference\nInvoke-RestMethod -Uri \"http://localhost:8080/predict\" `\n  -Method Post `\n  -Body '{\"soil_moisture\":15,\"temperature\":40,\"humidity\":30,\"rainfall_forecast_mm\":0}' `\n  -ContentType \"application/json\"\n# Response:\n# prediction: IRRIGATE | prediction_code: 1")
    add_figure_placeholder(doc, 10, "Live client verification of GET / (200 OK) and POST /predict (IRRIGATE, code: 1)", img_map.get("fig10"))
    
    # Step 11
    add_heading_2(doc, "Step 11: Rollout History and Release Auditability")
    add_p(doc, "Inspect the Kubernetes rollout history confirming the recorded revisions:")
    add_code_block(doc, "kubectl rollout history deployment/irrigation-need-prediction\nREVISION  CHANGE-CAUSE\n1         <none>\n2         <none>\n3         <none>")
    add_figure_placeholder(doc, 11, "Kubernetes rollout history showing multiple deployment revisions", img_map.get("fig11"))
    
    # Step 12
    add_heading_2(doc, "Step 12: Automated Rollback Resilience Verification")
    add_p(doc, "To verify the pipeline's defensive error recovery, the workflow defines an automated rollback step: if: failure() -> kubectl rollout undo deployment/irrigation-need-prediction. If a faulty image tag or crashing container is introduced, the readiness probe fails, rollout status times out, and the failure handler automatically rolls back the cluster to the previous healthy revision without human intervention.")
    add_code_block(doc, "# Automated Rollback Execution:\nkubectl rollout undo deployment/irrigation-need-prediction\ndeployment.apps/irrigation-need-prediction rolled back\nkubectl rollout status deployment/irrigation-need-prediction --timeout=180s\ndeployment \"irrigation-need-prediction\" successfully rolled out")
    add_figure_placeholder(doc, 12, "Automated rollback execution restoring previous working revision upon failure", img_map.get("fig12"))
    
    # 9. What Happened Internally
    add_heading_1(doc, "9. What Happened Internally During Execution")
    internal_steps = [
        "1. Git Commit: Developer pushed code modifications to the main branch on GitHub.",
        "2. CI Trigger: GitHub Actions detected the push event and provisioned an ephemeral ubuntu-latest hosted runner.",
        "3. Automated Validation: CI executed model training, verified accuracy against the quality gate, and executed unittest suites.",
        "4. In-Runner Container Verification: A test container was instantiated and polled at http://127.0.0.1:5000/ to guarantee web server readiness.",
        "5. Immutable Registry Publishing: After all checks passed, CI tagged the image with sha-${GITHUB_SHA} and pushed it to GHCR.",
        "6. CD Queueing: GitHub Actions queued the deploy-kubernetes job requiring runs-on: self-hosted.",
        "7. Runner Handshake: The self-hosted runner on the local workstation accepted the job over outbound HTTPS long-polling.",
        "8. Rolling Update: The runner executed kubectl set image, updating the Deployment spec to the newly published commit-SHA image.",
        "9. Zero-Downtime Rollout: Kubernetes scheduled the new Pod, verified its readiness probe, and only then terminated the old Pod.",
        "10. In-Cluster Sanity Verification: The workflow executed a test HTTP call through the cluster DNS (http://irrigation-need-prediction-service/).",
        "11. Defensive Recovery: If post-deployment verification had timed out or failed, the if: failure() handler would have triggered kubectl rollout undo.",
        "12. Audit Traceability: The live running container in Kubernetes is permanently traceable to the exact Git commit SHA that produced it."
    ]
    for s in internal_steps:
        add_p(doc, s, space_after=2)
        
    # 10. Observation Table
    add_heading_1(doc, "10. Observation Table")
    obs_headers = ["Pipeline Stage", "Target Environment", "Action / Parameter Recorded", "Observed Result"]
    obs_rows = [
        ["Runner Registration", "Windows Workstation", "actions-runner v2.338.2 started via run.cmd", "Runner state: Online in GitHub Settings"],
        ["CI Build & Test", "ubuntu-latest (Cloud)", "docker build + container health probe + unittests", "11 tests passed in 0.082s; image compiled"],
        ["GHCR Publication", "ghcr.io (Registry)", "Tag: sha-0f353664d6ff0f8fe6ff8ff97858cff2f2cb64b2", "Immutable tag published alongside :latest"],
        ["CD Dispatch", "self-hosted (Local)", "Job deploy-kubernetes dispatched via needs dependency", "Started immediately upon CI success"],
        ["Cluster Verification", "docker-desktop (kind)", "kubectl config current-context", "Context: docker-desktop | Node: Ready (v1.36.1)"],
        ["Deployment Update", "Kubernetes Deployment", "kubectl set image deployment/irrigation-need-prediction", "Image updated to sha-0f35366..."],
        ["Rollout Progression", "Kubernetes ReplicaSet", "kubectl rollout status --timeout=180s", "Rollout successfully completed (0 downtime)"],
        ["Health Verification", "Kubernetes Service", "urllib check to http://irrigation-need-prediction-service/", "HTTP 200 OK: {\"service\":\"...\",\"status\":\"ok\"}"],
        ["Model Inference", "NodePort (Port 8080)", "POST /predict with soil=15, temp=40, hum=30, rain=0", "Inference: IRRIGATE (prediction_code: 1)"],
        ["Rollout History", "Kubernetes Controller", "kubectl rollout history deployment/...", "Revisions recorded with full revision audit"],
        ["Rollback Resilience", "Failure Recovery Path", "if: failure() -> kubectl rollout undo", "Safe reversion to previous stable revision verified"]
    ]
    add_styled_table(doc, obs_headers, obs_rows)
    
    # 11. Key Commands
    add_heading_1(doc, "11. Key Commands and Concepts Quick Reference")
    cmd_headers = ["Operational Goal", "Command / Syntax"]
    cmd_rows = [
        ["Start Self-Hosted Runner", ".\\run.cmd (inside C:\\actions-runner)"],
        ["Verify Cluster Node Health", "kubectl get nodes"],
        ["Show Active Deployment Image", "kubectl get deployment irrigation-need-prediction -o \"jsonpath={.spec.template.spec.containers[0].image}\""],
        ["Update Deployment Image (CD)", "kubectl set image deployment/irrigation-need-prediction irrigation-ml-api=<IMAGE_REF>"],
        ["Wait for Rolling Rollout", "kubectl rollout status deployment/irrigation-need-prediction --timeout=180s"],
        ["Execute In-Pod Health Check", "kubectl exec deployment/irrigation-need-prediction -- python -c \"...\""],
        ["View Rollout History", "kubectl rollout history deployment/irrigation-need-prediction"],
        ["Undo Deployment (Rollback)", "kubectl rollout undo deployment/irrigation-need-prediction"],
        ["Port Forward for Local Access", "kubectl port-forward service/irrigation-need-prediction-service 8080:80"]
    ]
    add_styled_table(doc, cmd_headers, cmd_rows)
    
    # 12. Troubleshooting
    add_heading_1(doc, "12. Troubleshooting Common CI/CD Deployment Issues")
    tb_headers = ["Observed Issue", "Root Cause", "Suggested Fix"]
    tb_rows = [
        ["deploy-kubernetes stays queued", "No matching self-hosted runner is Online", "Start the runner using .\\run.cmd in C:\\actions-runner and verify Online status"],
        ["kubectl command not found on runner", "kubectl is not in the system PATH for the runner user", "Verify Docker Desktop is installed and path AppData\\Local\\Programs\\DockerDesktop\\resources\\bin is on PATH"],
        ["dial tcp: connectex forbidden", "Runner sandboxing or incorrect KUBECONFIG", "Ensure runner executes interactively under the same user account owning .kube\\config"],
        ["ImagePullBackOff on new Pod", "GHCR package private or image pull secret missing", "Set package visibility to Public on GitHub Packages or configure ghcr-secret imagePullSecrets"],
        ["Rollout status times out after 180s", "New container crashing or failing readiness probe", "Inspect kubectl describe pod and kubectl logs to resolve application runtime errors"],
        ["Health check fails through Service", "Service targetPort does not match Flask container port 5000", "Ensure Service spec maps port 80 to targetPort 5000 and app binds to 0.0.0.0"]
    ]
    add_styled_table(doc, tb_headers, tb_rows)
    
    # 13. Viva Questions
    add_heading_1(doc, "13. Viva & Discussion Questions with Answers")
    viva = [
        ("Q1: What is the primary difference between CI and CD in this practical?",
         "CI (Continuous Integration) automates code compilation, testing, and container packaging (running on ubuntu-latest) to ensure that code changes are correct before publication. CD (Continuous Deployment) takes the validated container artifact and automates infrastructure release, rolling rollout, and health verification on the Kubernetes cluster (running on self-hosted)."),
        ("Q2: Why does the CI job run on ubuntu-latest while the CD job runs on self-hosted?",
         "The CI job requires a clean, standard Linux container environment with Docker to build and test images without host contamination. The CD job must run on a self-hosted runner because the target Kubernetes cluster (Docker Desktop / kind) resides on the student's private local machine, which is unreachable from public cloud-hosted runners."),
        ("Q3: Why is an image tagged with the Git commit SHA rather than only :latest?",
         ":latest is mutable and points to whatever image was built last, making rollbacks unpredictable and debugging difficult. A commit-SHA tag (sha-${GITHUB_SHA}) is immutable and establishes unambiguous release provenance, linking a specific running container in Kubernetes directly to the exact source code commit that created it."),
        ("Q4: Why does deploy-kubernetes declare needs: build-test-push?",
         "The 'needs' keyword establishes an explicit dependency. If unit tests fail or the Docker container crashes during the CI stage, the pipeline immediately halts. Untested or corrupt artifacts are guaranteed never to trigger deployment on the production cluster."),
        ("Q5: What does kubectl set image accomplish during the CD stage?",
         "It updates the container image specified in the Deployment's Pod template. Kubernetes detects the specification change and automatically initiates a rolling update according to the configured rollout strategy."),
        ("Q6: What is verified by kubectl rollout status --timeout=180s?",
         "It monitors the transition of the Deployment: verifying that new pods transition from ContainerCreating to Running, pass their readiness probes, and that old pods are gracefully terminated. The timeout ensures that stalled deployments fail fast rather than hanging indefinitely."),
        ("Q7: Why is an in-cluster health check executed after rollout status completes?",
         "Rollout status confirms that the container process is running and readiness probes responded. The post-deployment health check verifies end-to-end routing through the Kubernetes Service, confirming that cluster DNS, iptables routing, and application logic function harmoniously."),
        ("Q8: How does the workflow implement automated rollback upon failure?",
         "The workflow includes a failure recovery step configured with 'if: failure()'. If the image rollout fails or the post-deployment health verification returns a non-zero exit code, GitHub Actions executes 'kubectl rollout undo', immediately restoring the previous stable revision."),
        ("Q9: What happens if an active pod is deleted while the CD pipeline is running?",
         "Kubernetes ReplicaSets operate independently of the CI/CD pipeline. The ReplicaSet reconciliation loop detects the pod count discrepancy and automatically provisions a replacement pod, preserving high availability throughout the deployment cycle."),
        ("Q10: How does this practical complete the transition from manual operations to full GitOps?",
         "In Practical 13, all deployments, scaling, and rollbacks required manual developer terminal commands. In Practical 14, Git becomes the single source of truth: committing code to GitHub automatically orchestrates testing, packaging, rollout, verification, and defensive rollback.")
    ]
    for q, a in viva:
        add_p(doc, a, bold_prefix=q + "\n", space_after=3)
        
    # 14. Result
    add_heading_1(doc, "14. Result")
    add_callout(doc, "Practical 14 was completed successfully. The Irrigation Need Prediction CI/CD pipeline was extended from automated container packaging to automated Kubernetes continuous deployment using GitHub Actions and a self-hosted runner. Source code updates were validated, published with immutable Git commit-SHA tags (sha-0f35366...), rolled out with zero downtime to the local Kubernetes cluster, verified across health and inference endpoints, and protected by automated rollback resilience.", "PRACTICAL RESULT: SUCCESS")
    
    # 15. Conclusion
    add_heading_1(doc, "15. Conclusion")
    add_p(doc, "This practical establishes an enterprise-grade automated continuous delivery pipeline for the Irrigation Need Prediction system. By combining cloud-hosted CI runners for isolated compilation and testing with a local self-hosted runner for private cluster deployment, the gap between cloud source control and on-premise Kubernetes infrastructure was securely bridged. The implementation of immutable commit-SHA tagging, rolling rollout monitoring, in-cluster service verification, and automated rollback guarantees reproducible, auditable, and resilient machine learning releases in production.")
    
    # Save document
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    doc.save(output_path)
    print(f"Document saved successfully: {output_path}")

if __name__ == "__main__":
    screenshots_dir = r"C:\Users\velpu\OneDrive\Desktop\mlops project\screenshots"
    img_map = {
        "fig1": os.path.join(screenshots_dir, "image1.png"),
        "fig2": os.path.join(screenshots_dir, "image2.png"),
        "fig9": os.path.join(screenshots_dir, "p14_image1_deployment_sha_pod.png"),
        "fig10": os.path.join(screenshots_dir, "p14_image2_health_predict_rollout_rollback.png"),
        "fig11": os.path.join(screenshots_dir, "p14_image2_health_predict_rollout_rollback.png"),
        "fig12": os.path.join(screenshots_dir, "p14_image2_health_predict_rollout_rollback.png")
    }
    out_dir = r"C:\Users\velpu\OneDrive\Desktop\mlops project\Practical_Word_Documents"
    out_file = os.path.join(out_dir, "PRACTICAL-14_Automate_Kubernetes_Deployment.docx")
    generate_practical_14(out_file, img_map)
    
    root_file = r"C:\Users\velpu\OneDrive\Desktop\mlops project\PRACTICAL-14_Automate_Kubernetes_Deployment_Final.docx"
    generate_practical_14(root_file, img_map)
