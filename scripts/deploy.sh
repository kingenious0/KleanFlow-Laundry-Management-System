#!/usr/bin/env bash
# Production Deployment Automation Script for KleanFlow Laundry Management System (Linux/Unix)

set -e

echo "========================================================="
echo "  KleanFlow Laundry Management System — Deployment Setup "
echo "========================================================="

# Step 1: Ensure virtual environment exists and is activated
if [ ! -d "venv" ]; then
    echo "[1/5] Creating Python virtual environment..."
    python3 -m venv venv
fi

echo "[1/5] Activating virtual environment..."
source venv/bin/activate

# Step 2: Install/upgrade dependencies
echo "[2/5] Installing production dependencies from requirements.txt..."
pip install --upgrade pip
pip install -r requirements.txt

# Step 3: Ensure environment file exists
if [ ! -f ".env" ]; then
    echo "NOTICE: .env file not found. Copying from .env.example..."
    cp .env.example .env
    echo "WARNING: Please edit .env to set your production database credentials and SECRET_KEY before running in production!"
fi

# Step 4: Run Flask database migrations
echo "[3/5] Applying database migrations..."
export FLASK_APP=run.py
flask db upgrade

# Step 5: Bootstrapping Administrator Account
echo "[4/5] Checking Administrator bootstrap..."
python scripts/create_admin.py --email admin@kleanflow.com --name "System Administrator" --phone 0200000000 --password "AdminPass123!" || true

# Step 6: Start Gunicorn WSGI Server
echo "[5/5] Launching Gunicorn WSGI production server..."
exec gunicorn -c gunicorn.conf.py run:app
