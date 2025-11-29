#!/usr/bin/env bash
set -e

echo "Downloading ML files from Google Drive..."
python download_ml_files.py

echo "Starting FastAPI with Uvicorn..."
uvicorn backend.app:app --host 0.0.0.0 --port $PORT
