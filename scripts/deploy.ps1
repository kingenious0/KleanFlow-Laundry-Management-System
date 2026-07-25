# Production Deployment Automation Script for KleanFlow Laundry Management System (Windows PowerShell)

$ErrorActionPreference = "Stop"

Write-Host "=========================================================" -ForegroundColor Cyan
Write-Host "  KleanFlow Laundry Management System — Deployment Setup " -ForegroundColor Cyan
Write-Host "=========================================================" -ForegroundColor Cyan

# Step 1: Ensure virtual environment exists
if (-not (Test-Path "venv")) {
    Write-Host "[1/5] Creating Python virtual environment..." -ForegroundColor Yellow
    python -m venv venv
}

Write-Host "[1/5] Activating virtual environment..." -ForegroundColor Yellow
& .\venv\Scripts\Activate.ps1

# Step 2: Install/upgrade dependencies
Write-Host "[2/5] Installing production dependencies from requirements.txt..." -ForegroundColor Yellow
pip install --upgrade pip
pip install -r requirements.txt

# Step 3: Ensure environment file exists
if (-not (Test-Path ".env")) {
    Write-Host "NOTICE: .env file not found. Copying from .env.example..." -ForegroundColor Yellow
    Copy-Item ".env.example" ".env"
    Write-Host "WARNING: Please edit .env to set your production database credentials and SECRET_KEY!" -ForegroundColor Red
}

# Step 4: Run Flask database migrations
Write-Host "[3/5] Applying database migrations..." -ForegroundColor Yellow
$env:FLASK_APP = "run.py"
flask db upgrade

# Step 5: Bootstrapping Administrator Account
Write-Host "[4/5] Checking Administrator bootstrap..." -ForegroundColor Yellow
python scripts/create_admin.py --email admin@kleanflow.com --name "System Administrator" --phone 0200000000 --password "AdminPass123!"

# Step 6: Start Application
Write-Host "[5/5] Launching KleanFlow server..." -ForegroundColor Green
python run.py
