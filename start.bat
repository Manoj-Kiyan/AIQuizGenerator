@echo off
echo ===================================================
echo Starting QuizAI Setup and Server
echo ===================================================

:: Check if Python is installed
python --version >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Python is not installed or not in PATH!
    echo Please install Python 3.9+ and try again.
    pause
    exit /b
)

:: Check if venv exists
IF NOT EXIST "venv\Scripts\activate.bat" (
    echo [INFO] Creating Virtual Environment...
    python -m venv venv
) ELSE (
    echo [INFO] Virtual Environment already exists.
)

:: Activate venv and install requirements
echo [INFO] Activating venv and installing requirements...
call venv\Scripts\activate.bat
python -m pip install --upgrade pip
pip install -r requirements.txt

:: Start the FastAPI server
echo [INFO] Starting FastAPI server on http://localhost:8000...
echo ===================================================
uvicorn backend.main:app --reload
