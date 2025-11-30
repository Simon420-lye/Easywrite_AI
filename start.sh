#!/bin/bash

# Start FastAPI backend in the background
uvicorn app:app --host 0.0.0.0 --port 8000 &

# Wait a moment for FastAPI to start
sleep 2

# Start Streamlit frontend (this keeps the container running)
streamlit run ui.py --server.port=8501 --server.address=0.0.0.0 --server.headless=true