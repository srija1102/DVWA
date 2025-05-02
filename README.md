

# AI-Augmented DevSecOps Pipeline for Cloud-Native Applications

This repository implements an adaptive DevSecOps pipeline that integrates automated security scanning (Checkov, Trivy, OWASP ZAP) with an AI-based threat classification script to enhance vulnerability management and reduce false positives in CI/CD workflows.

---

## 📦 What It Does

✅ Automates build, security scanning, deployment, and reporting using GitHub Actions.  
✅ Runs infrastructure, container, and web application vulnerability scans.  
✅ Uses a Python machine learning script to classify threat severity (low/high) and generate actionable summaries.  
✅ Deploys the application to AWS EKS securely using Kubernetes manifests.  
✅ Sends email notifications with summary results and attached scan reports.

---

## 🔧 Dependencies & Setup

Before you run the pipeline, ensure:

1️⃣ **GitHub repository setup**  
- Add the following repository secrets:
  - `AWS_ACCESS_KEY_ID`  
  - `AWS_SECRET_ACCESS_KEY`  
  - `AWS_REGION`  
  - `EKS_CLUSTER_NAME`  
  - `LOAD_BALANCER_URL`  
  - `MAIL_USERNAME` (email account)  
  - `MAIL_PASSWORD` (email password or app token)  
  - `MAIL_RECIPIENT` (your recipient email address)

2️⃣ **AWS EKS cluster is running**  
- Ensure you have a working Kubernetes cluster (EKS) and access configured.

3️⃣ **Python script requirements**  
- The GitHub Actions pipeline installs `pandas` and `scikit-learn` automatically (no local install required).

---

## 🚀 How to Run

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/your-repo.git
   cd your-repo
   ```

2. Push any code changes to trigger the pipeline:
   ```bash
   git push origin main
   ```

3. Go to **GitHub → Actions** to monitor the pipeline stages:
   - **Build & Scan** → Runs Checkov, Trivy, ZAP
   - **Classify** → Runs Python AI script
   - **Deploy** → Pushes Docker image and applies Kubernetes manifests
   - **Notify** → Sends email report

4. Retrieve full log artifacts:
   - Available under **Actions → Artifacts → security-logs.zip**

---

## 📂 Folder Structure

```
.
├── .github/workflows/deploy.yml    # CI/CD pipeline
├── kube/                           # Kubernetes manifests
├── scripts/                        # classify_threats.py (ML script)
├── logs/                           # Output folder (created at runtime)
├── Dockerfile                      # Application container
└── README.md                       # Project overview and instructions
```

---

## 🏗️ Setup Tools (Handled by Pipeline)

- **Checkov** → `pip install checkov`  
- **Trivy** → Downloaded & installed inside pipeline  
- **OWASP ZAP** → Runs inside GitHub Action container  
- **Python ML** → Uses `pandas` and `scikit-learn` (installed in pipeline)

You don’t need to install these manually unless you want to run scans locally.

---

## 📊 Example Outputs

| Tool      | Example Finding                          |
|-----------|-----------------------------------------|
| Checkov   | 851 low severity, 77 high severity misconfigs |
| Trivy     | ~300 container issues detected          |
| ZAP       | 12 new warnings, no critical failures   |
| Classifier| Summarized CSV of high vs. low threats  |

Artifacts include:
- `classified_results.csv`  
- `checkov.json`  
- `trivy_results.json`  
- `zap_results.json`  
- `zap_report.html`

---

## 📈 Future Improvements

- Integrate advanced anomaly detection models.  
- Extend to multi-cloud (Azure, GCP) deployments.  
- Add dashboards (Grafana, Power BI) for live visualization.  
- Automate remediation scripts for critical findings.

---

