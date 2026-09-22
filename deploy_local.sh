#!/usr/bin/env bash
echo "=== Starting MediKiosk Locally ==="
pip install -r requirements.txt
export PORT=7860
python3 -m uvicorn backend.main:app --host 0.0.0.0 --port 7860 --reload
