#!/usr/bin/env bash
python download_ml_files.py
uvicorn backend.app:app --host 0.0.0.0 --port $PORT
