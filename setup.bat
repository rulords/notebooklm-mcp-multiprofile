@echo off
echo ======================================================
echo   NotebookLM MCP - Setup Script
echo ======================================================
echo.

:: Check for Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python not found. Please install Python 3.10 or higher.
    pause
    exit /b 1
)

:: Create Virtual Environment
if not exist .venv (
    echo [1/3] Creating virtual environment...
    python -m venv .venv
) else (
    echo [1/3] Virtual environment already exists.
)

:: Install Requirements
echo [2/3] Installing dependencies...
.venv\Scripts\python -m pip install --upgrade pip
.venv\Scripts\pip install -r requirements.txt

:: Check for common errors (Python 3.12+)
.venv\Scripts\python -c "import setuptools" >nul 2>&1
if %errorlevel% neq 0 (
    echo [INFO] Installing setuptools for compatibility...
    .venv\Scripts\pip install setuptools
)

echo.
echo [3/3] Setup complete!
echo.
echo Proximos pasos:
echo 1. Sigue la guia en docs\AUTHENTICATION.md para tus cookies.
echo 2. Corre 'python verify_profile.py' para chequear el estado.
echo.
pause
