#!/usr/bin/env bash
# ==============================================================================
# KleanFlow Laundry Management System
# Production Deployment Script — Linux / Unix (Nginx + Gunicorn)
# ==============================================================================
# Usage:
#   chmod +x scripts/deploy.sh
#   ./scripts/deploy.sh
#
# Requirements:
#   - Python 3.13+
#   - MySQL 8.0+ running and configured in .env
#   - Nginx installed (optional but recommended for reverse proxy)
# ==============================================================================

set -euo pipefail

APP_NAME="kleanflow"
APP_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
VENV_DIR="${APP_DIR}/venv"
LOG_DIR="${APP_DIR}/logs"
BACKUP_DIR="${APP_DIR}/backups"

echo "========================================================="
echo "  KleanFlow Laundry Management System — Deployment Setup "
echo "========================================================="
echo ""
echo "  App Directory : ${APP_DIR}"
echo "  Environment   : ${FLASK_ENV:-production}"
echo ""

# ── Step 1: Virtual Environment ──────────────────────────────────────────────
echo "[1/6] Setting up Python virtual environment..."
if [ ! -d "${VENV_DIR}" ]; then
    python3 -m venv "${VENV_DIR}"
    echo "      Virtual environment created at ${VENV_DIR}"
fi
# shellcheck source=/dev/null
source "${VENV_DIR}/bin/activate"
echo "      Virtual environment activated."

# ── Step 2: Install Dependencies ─────────────────────────────────────────────
echo "[2/6] Installing production dependencies..."
pip install --upgrade pip --quiet
pip install -r "${APP_DIR}/requirements.txt" --quiet
echo "      Dependencies installed successfully."

# ── Step 3: Environment Configuration ────────────────────────────────────────
echo "[3/6] Checking environment configuration..."
if [ ! -f "${APP_DIR}/.env" ]; then
    echo "      NOTICE: .env file not found. Copying from .env.example..."
    cp "${APP_DIR}/.env.example" "${APP_DIR}/.env"
    echo ""
    echo "  ⚠️  WARNING: Production .env created from template."
    echo "  ⚠️  Edit ${APP_DIR}/.env and set:"
    echo "      - SECRET_KEY (strong random key)"
    echo "      - MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DATABASE"
    echo ""
    read -rp "  Press ENTER to continue or Ctrl+C to abort and edit .env first..."
fi
echo "      Environment configuration OK."

# ── Step 4: Directory Setup ───────────────────────────────────────────────────
echo "[4/6] Creating required directories..."
mkdir -p "${LOG_DIR}" "${BACKUP_DIR}" "${APP_DIR}/uploads"
touch "${LOG_DIR}/.gitkeep" "${BACKUP_DIR}/.gitkeep" "${APP_DIR}/uploads/.gitkeep" 2>/dev/null || true
echo "      Directories ready."

# ── Step 5: Database Migration ────────────────────────────────────────────────
echo "[5/6] Applying database schema migrations..."
export FLASK_APP="${APP_DIR}/run.py"
cd "${APP_DIR}"
flask db upgrade
echo "      Database migrations applied."

# Bootstrap Administrator account (safe to re-run; skips if admin exists)
echo "      Bootstrapping Administrator account (skips if already exists)..."
python "${APP_DIR}/scripts/create_admin.py" \
    --email admin@kleanflow.com \
    --name "System Administrator" \
    --phone 0200000000 \
    --password "AdminPass123!" || true

# ── Step 6: Start Gunicorn ────────────────────────────────────────────────────
echo "[6/6] Launching Gunicorn WSGI production server..."
echo ""
echo "  Server will bind to: $(grep GUNICORN_BIND ${APP_DIR}/.env 2>/dev/null | cut -d= -f2 || echo '0.0.0.0:5000')"
echo ""
exec gunicorn -c "${APP_DIR}/gunicorn.conf.py" run:app
