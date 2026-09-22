# MediKiosk - AI Clinical History Platform

MediKiosk is an AI-powered, multimodal clinical intake platform designed for high-density outpatient departments (OPDs) in Indian allopathic and AYUSH hospitals.

## 🚀 100% Free 1-Click Cloud Deployment (Hugging Face Spaces)
1. Go to [Hugging Face Spaces](https://huggingface.co/spaces) and click **Create new Space**.
2. Select **Docker** as the Space SDK and choose the **Blank** template. (Keep it Public and Free CPU).
3. Clone or upload the repository files (`Dockerfile`, `requirements.txt`, `backend/`, `frontend/`).
4. Hugging Face automatically builds the Docker container and serves your application at a permanent live HTTPS URL (e.g. `https://yourusername-medikiosk.hf.space`) with **zero cost, zero subscriptions, and no credit card required**.

## 💻 Local Hospital PC Deployment
```bash
# 1. Install system Tesseract OCR (if using local image scanning)
sudo apt-get update && sudo apt-get install -y tesseract-ocr tesseract-ocr-hin

# 2. Run local setup script
chmod +x deploy_local.sh
./deploy_local.sh
```
Open `http://localhost:7860` in your web browser.
