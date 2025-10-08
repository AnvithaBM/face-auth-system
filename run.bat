@echo off
REM Start the Face Authentication System

echo ==================================================
echo Face Authentication System
echo ==================================================
echo.

REM Check if virtual environment exists
if not exist "venv" (
    echo Virtual environment not found. Creating one...
    python -m venv venv
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Check if dependencies are installed
echo Checking dependencies...
pip list | findstr Flask >nul
if errorlevel 1 (
    echo Installing dependencies...
    pip install -r requirements.txt
)

REM Start the application
echo.
echo Starting Face Authentication System...
echo Access the application at: http://localhost:5000
echo.
echo Press Ctrl+C to stop the server
echo ==================================================
echo.

python app.py
