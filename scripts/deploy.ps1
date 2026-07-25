# ==============================================================================
# KleanFlow Laundry Management System
# Production Deployment Script — Windows Server (PowerShell 5+)
# ==============================================================================
# Usage:
#   Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
#   .\scripts\deploy.ps1
#
# Requirements:
#   - Python 3.13+
#   - MySQL 8.0+ running and configured in .env
# ==============================================================================

$ErrorActionPreference = "Stop"

$AppDir     = Resolve-Path (Join-Path $PSScriptRoot "..")
$VenvDir    = Join-Path $AppDir "venv"
$LogDir     = Join-Path $AppDir "logs"
$BackupDir  = Join-Path $AppDir "backups"
$UploadsDir = Join-Path $AppDir "uploads"

Write-Host ""
Write-Host "=========================================================" -ForegroundColor Cyan
Write-Host "  KleanFlow Laundry Management System — Deployment Setup " -ForegroundColor Cyan
Write-Host "=========================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "  App Directory : $AppDir" -ForegroundColor Gray
Write-Host ""

# ── Step 1: Virtual Environment ──────────────────────────────────────────────
Write-Host "[1/6] Setting up Python virtual environment..." -ForegroundColor Yellow
if (-not (Test-Path $VenvDir)) {
    python -m venv $VenvDir
    Write-Host "      Virtual environment created at $VenvDir" -ForegroundColor Gray
}
& "$VenvDir\Scripts\Activate.ps1"
Write-Host "      Virtual environment activated." -ForegroundColor Green

# ── Step 2: Install Dependencies ─────────────────────────────────────────────
Write-Host "[2/6] Installing production dependencies..." -ForegroundColor Yellow
pip install --upgrade pip --quiet
pip install -r (Join-Path $AppDir "requirements.txt") --quiet
Write-Host "      Dependencies installed successfully." -ForegroundColor Green

# ── Step 3: Environment Configuration ────────────────────────────────────────
Write-Host "[3/6] Checking environment configuration..." -ForegroundColor Yellow
$EnvFile = Join-Path $AppDir ".env"
if (-not (Test-Path $EnvFile)) {
    Copy-Item (Join-Path $AppDir ".env.example") $EnvFile
    Write-Host ""
    Write-Host "  WARNING: .env created from template." -ForegroundColor Red
    Write-Host "  REQUIRED: Edit $EnvFile and set:" -ForegroundColor Red
    Write-Host "    - SECRET_KEY (use a strong random string)" -ForegroundColor Red
    Write-Host "    - MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DATABASE" -ForegroundColor Red
    Write-Host ""
    Read-Host "  Press ENTER to continue or Ctrl+C to abort and configure .env first"
}
Write-Host "      Environment configuration OK." -ForegroundColor Green

# ── Step 4: Directory Setup ───────────────────────────────────────────────────
Write-Host "[4/6] Creating required directories..." -ForegroundColor Yellow
@($LogDir, $BackupDir, $UploadsDir) | ForEach-Object {
    if (-not (Test-Path $_)) { New-Item -ItemType Directory -Path $_ | Out-Null }
}
Write-Host "      Directories ready." -ForegroundColor Green

# ── Step 5: Database Migration ────────────────────────────────────────────────
Write-Host "[5/6] Applying database schema migrations..." -ForegroundColor Yellow
$env:FLASK_APP = "run.py"
Set-Location $AppDir
flask db upgrade
Write-Host "      Database migrations applied." -ForegroundColor Green

Write-Host "      Bootstrapping Administrator account..." -ForegroundColor Gray
try {
    python (Join-Path $AppDir "scripts\create_admin.py") `
        --email admin@kleanflow.com `
        --name "System Administrator" `
        --phone 0200000000 `
        --password "AdminPass123!"
} catch {
    Write-Host "      Admin already exists — skipping." -ForegroundColor Gray
}

# ── Step 6: Launch Server ─────────────────────────────────────────────────────
Write-Host "[6/6] Launching KleanFlow server..." -ForegroundColor Yellow
Write-Host ""
Write-Host "  Application is starting at http://127.0.0.1:5000" -ForegroundColor Cyan
Write-Host "  Press Ctrl+C to stop the server." -ForegroundColor Gray
Write-Host ""

# Use Gunicorn if available (for Windows Subsystem for Linux), else fallback to Flask dev server
try {
    gunicorn -c (Join-Path $AppDir "gunicorn.conf.py") run:app
} catch {
    Write-Host "  Gunicorn not available on native Windows. Starting Flask development server..." -ForegroundColor Yellow
    Write-Host "  For production on Windows, use WSL2 + Gunicorn or deploy to Linux server." -ForegroundColor Yellow
    python (Join-Path $AppDir "run.py")
}
