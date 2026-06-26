#!/bin/bash

echo "==================================================="
echo "Starting QuizAI Setup and Server"
echo "==================================================="

# Check if python3 is installed
if ! command -v python3 &> /dev/null
then
    echo "[ERROR] python3 could not be found. Please install Python 3.9+"
    exit 1
fi

# Check if venv exists
if [ ! -f "venv/bin/activate" ]; then
    echo "[INFO] Creating Virtual Environment..."
    python3 -m venv venv
else
    echo "[INFO] Virtual Environment already exists."
fi

# Activate venv and install requirements
echo "[INFO] Activating venv and installing requirements..."
source venv/bin/activate
python3 -m pip install --upgrade pip
pip install -r requirements.txt

# Start the FastAPI server
echo "[INFO] Starting FastAPI server on http://localhost:8000..."
echo "==================================================="
uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload
