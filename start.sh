#!/usr/bin/env bash

echo "Downloading ML files..."
python ../download_ml_files.py

echo "Starting FastAPI..."
uvicorn app:app --host 0.0.0.0 --port $PORT
