#!/bin/bash
echo "======================================================"
echo "  NotebookLM MCP - Setup Script (Linux/macOS)"
echo "======================================================"
echo ""

# Check for Python
if ! command -v python3 &> /dev/null; then
    echo "[ERROR] Python3 not found. Please install Python 3.10 or higher."
    exit 1
fi

# Need python3-venv installed on Debian/Ubuntu
if ! python3 -c "import venv" &> /dev/null; then
    echo "[ERROR] python3-venv is missing. Install it using:"
    echo "sudo apt install python3-venv"
    exit 1
fi

# Create Virtual Environment
if [ ! -d ".venv" ]; then
    echo "[1/3] Creating virtual environment..."
    python3 -m venv .venv
else
    echo "[1/3] Virtual environment already exists."
fi

# Install Requirements
echo "[2/3] Installing dependencies..."
.venv/bin/python -m pip install --upgrade pip
.venv/bin/pip install -r requirements.txt

echo ""
echo "[3/3] Setup complete!"
echo ""
echo "Proximos pasos:"
echo "1. Sigue la guia en docs/AUTHENTICATION.md para tus cookies."
echo "2. Corre '.venv/bin/python verify_profile.py' para chequear el estado."
echo ""
