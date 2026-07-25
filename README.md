# KleanFlow — Laundry Management System

[![Tests](https://img.shields.io/badge/tests-81%20passed-brightgreen.svg)](#-automated-tests)
[![Python](https://img.shields.io/badge/python-3.13%2B-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.0%2B-black.svg)](https://flask.palletsprojects.com/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

**KleanFlow** is a production-ready, web-based Laundry Management System built for small and medium-sized laundry and dry-cleaning businesses in Ghana. It manages the complete operational workflow — from customer walk-in to order completion, payment, and pickup/delivery logistics — with a role-based access control system that keeps every team member focused on exactly what they need to do.

---

## 🌟 Features At a Glance

| # | Feature | Description |
|---|---------|-------------|
| 1 | **User & RBAC** | 4 roles: `Administrator`, `Manager`, `Cashier`, `Staff` |
| 2 | **Customer Management** | Auto-generated customer codes, search, order history |
| 3 | **Service Catalog** | Priced services with GH₵ currency, enable/disable |
| 4 | **Order Workflow** | 6-stage lifecycle: Pending → Received → Washing → Ironing → Ready → Completed |
| 5 | **Payments & Receipts** | Multiple payment methods, auto receipt generation, PDF-ready print |
| 6 | **Pickup & Delivery** | Scheduling with staff assignment, status tracking |
| 7 | **Dashboard & Reports** | Real-time KPIs, Chart.js visualizations, CSV exports |
| 8 | **Security** | CSRF, XSS, SQL-injection protection; rate-limited login; session hardening |

---

## 🔐 Role Permissions

| Permission | Admin | Manager | Cashier | Staff |
|-----------|:-----:|:-------:|:-------:|:-----:|
| Manage Users | ✅ | ❌ | ❌ | ❌ |
| Manage Customers | ✅ | ✅ | ✅ | ❌ |
| Manage Services | ✅ | ✅ | ❌ | ❌ |
| Create / View Orders | ✅ | ✅ | ✅ | ✅ |
| Process Payments | ✅ | ✅ | ✅ | ❌ |
| Pickup & Delivery | ✅ | ✅ | ✅ | ✅ |
| View Dashboard | ✅ | ✅ | ❌ | ❌ |
| View Reports | ✅ | ✅ | ❌ | ❌ |

---

## 🏗️ Technology Stack

- **Backend:** Python 3.13+, Flask 3.0+, SQLAlchemy 2.0+, Flask-Migrate, Flask-Login, Flask-WTF
- **Frontend:** HTML5, Bootstrap 5.3, Chart.js 4.4, Remix Icons, Vanilla CSS
- **Database:** MySQL 8.0+ (Production) / SQLite (Development & Testing)
- **WSGI Server:** Gunicorn 23.0+ (Linux), Flask dev server (Windows dev)
- **Testing:** pytest 8.0+, 81 tests across 11 test modules

---

## 📁 Project Structure

```
KleanFlow Laundry Management System/
├── app/
│   ├── auth/                  # Authentication Blueprint (login/logout)
│   ├── blueprints/
│   │   ├── customers/         # Customer CRUD
│   │   ├── dashboard/         # Dashboard KPIs & charts
│   │   ├── logistics/         # Pickup & Delivery
│   │   ├── orders/            # Order creation & workflow
│   │   ├── payments/          # Payment recording & receipts
│   │   ├── reports/           # Revenue & customer reports + CSV export
│   │   ├── services/          # Service catalog
│   │   └── users/             # User management (admin only)
│   ├── models/                # SQLAlchemy ORM models
│   ├── repositories/          # Data Access Layer (Repository Pattern)
│   ├── services_layer/        # Business Logic Layer
│   ├── validators/            # Input & business-rule validation
│   ├── static/                # CSS, JS, images
│   ├── templates/             # Jinja2 HTML templates
│   ├── config.py              # Development / Testing / Production configs
│   └── extensions.py          # Flask extension initialization
├── docs/                      # Architecture, SRS, API specs (18 documents)
├── migrations/                # Flask-Migrate Alembic migration files
├── scripts/
│   ├── create_admin.py        # One-time admin bootstrap script
│   ├── backup_db.py           # Database backup utility
│   ├── deploy.sh              # Linux production deployment script
│   ├── deploy.ps1             # Windows deployment script
│   ├── nginx.conf             # Nginx reverse proxy configuration
│   └── kleanflow.service      # Systemd service unit file
├── tests/                     # pytest test suites (81 tests)
├── .env.example               # Environment variable template
├── gunicorn.conf.py           # Gunicorn production server configuration
├── requirements.txt           # Python dependencies
└── run.py                     # Application entry point
```

---

## 🚀 Quick Start (Local Development)

### Prerequisites
- Python 3.13+
- Git

### 1. Clone the Repository
```bash
git clone https://github.com/kingenious0/KleanFlow-Laundry-Management-System.git
cd "KleanFlow Laundry Management System"
```

### 2. Create a Virtual Environment
```bash
# Linux / macOS
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment
```bash
cp .env.example .env
```
The default `.env` uses SQLite — **no database installation needed** for local testing.
For MySQL, edit the `MYSQL_*` values in `.env`.

### 5. Initialize Database & Create Admin
```bash
flask db upgrade
python scripts/create_admin.py --email admin@kleanflow.com --name "System Administrator" --phone 0200000000 --password "AdminPass123!"
```

### 6. Run the Development Server
```bash
python run.py
```
Open **http://localhost:5000** and log in with `admin@kleanflow.com` / `AdminPass123!`.

---

## 🎯 Real-World Workflow

### Customer Walk-In Scenario
1. **Cashier / Manager** opens *Customers* → searches for existing customer or creates a new one.
2. **Cashier / Manager** opens *New Order* → selects the customer → adds laundry items and services → submits.
3. Order starts at **Pending** status.
4. **Staff / Manager** advances the order through: `Received` → `Washing` → `Ironing` → `Ready`.
5. **Cashier** records a payment (full or partial) — a receipt number is auto-generated.
6. Order is marked **Completed** when the customer collects their laundry.

### Pickup & Delivery Scenario
1. Customer requests pickup → **Manager/Cashier** creates a *Pickup* record, assigns an available Staff driver.
2. Driver picks up laundry → status updated to **In Transit**.
3. Laundry processed through normal order workflow.
4. **Manager/Cashier** schedules a *Delivery*, assigns driver.
5. Driver delivers → status updated to **Completed**.

### Admin Scenario
1. **Administrator** creates user accounts, assigns roles.
2. Sets up the **Service Catalog** with pricing in GH₵.
3. Monitors the **Dashboard** for real-time KPIs.
4. Exports **Revenue Reports** or **Customer Reports** as CSV.

---

## 🧪 Automated Tests

81 tests across 11 modules covering validators, models, services, routes, security, and full E2E workflows:

```bash
# Run all tests
python -m pytest

# Run specific module
python -m pytest tests/test_security.py -v
python -m pytest tests/test_integration_workflows.py -v

# Run with coverage report
pip install pytest-cov
python -m pytest --cov=app --cov-report=term-missing
```

| Test Module | Coverage |
|-------------|----------|
| `test_foundation.py` | App creation, extensions, config |
| `test_auth.py` | Login, logout, session management |
| `test_users.py` | User CRUD, role assignment, RBAC |
| `test_customers.py` | Customer CRUD, code generation, search |
| `test_services.py` | Service catalog CRUD, validation |
| `test_orders.py` | Order creation, status workflow, cancellation |
| `test_payments.py` | Payment recording, receipt generation |
| `test_dashboard_reports.py` | KPI data, charts, reports, CSV export |
| `test_validators.py` | All validator rules |
| `test_security.py` | CSRF, auth boundaries, injection protection |
| `test_integration_workflows.py` | Full E2E business lifecycle |

---

## 📦 Production Deployment

### Linux Server (Recommended — Nginx + Gunicorn + systemd)

**Step 1 — Run the deployment script:**
```bash
chmod +x scripts/deploy.sh
./scripts/deploy.sh
```

**Step 2 — Install systemd service:**
```bash
sudo cp scripts/kleanflow.service /etc/systemd/system/kleanflow.service
# Edit the file to set correct User, WorkingDirectory paths
sudo systemctl daemon-reload
sudo systemctl enable kleanflow
sudo systemctl start kleanflow
sudo systemctl status kleanflow
```

**Step 3 — Configure Nginx:**
```bash
sudo cp scripts/nginx.conf /etc/nginx/sites-available/kleanflow
# Edit server_name and static file path
sudo ln -s /etc/nginx/sites-available/kleanflow /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

**Step 4 — Secure with SSL (Let's Encrypt):**
```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com
```

---

### Windows Server (PowerShell)
```powershell
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
.\scripts\deploy.ps1
```

> **Note:** Gunicorn does not run natively on Windows. For production on Windows, use WSL2 with the Linux deployment method, or use IIS as the reverse proxy with `waitress` as the WSGI server.

---

### Essential Production `.env` Settings

```env
FLASK_ENV=production
SECRET_KEY=<generate-with: python -c "import secrets; print(secrets.token_hex(64))">
SESSION_COOKIE_SECURE=True

MYSQL_HOST=localhost
MYSQL_USER=kleanflow_user
MYSQL_PASSWORD=<strong-password>
MYSQL_DATABASE=kleanflow_db

GUNICORN_WORKERS=5
GUNICORN_BIND=0.0.0.0:5000
```

---

## 🔒 Security Checklist (Before Going Live)

- [ ] `SECRET_KEY` set to a cryptographically random value (64+ hex chars)
- [ ] `FLASK_ENV=production`
- [ ] `SESSION_COOKIE_SECURE=True` (requires HTTPS)
- [ ] MySQL user has **minimum required privileges** (`SELECT, INSERT, UPDATE, DELETE` on `kleanflow_db.*` only)
- [ ] Default admin password changed from `AdminPass123!`
- [ ] Firewall rules: only expose ports 80 and 443 (Nginx handles traffic to Gunicorn on 5000)
- [ ] SSL/TLS certificate installed (Let's Encrypt recommended)
- [ ] `logs/` directory writable by the service user
- [ ] `.env` not readable by other users (`chmod 600 .env`)
- [ ] Database backups scheduled: `python scripts/backup_db.py`

---

## 🗄️ Database Backup

```bash
# Manual backup
python scripts/backup_db.py

# Schedule daily backup via cron (Linux)
crontab -e
# Add:  0 2 * * * cd /var/www/kleanflow && venv/bin/python scripts/backup_db.py
```

Backups are stored in `backups/` as timestamped SQL dump files.

---

## 📄 Documentation

All specification and design documents are in the `docs/` directory:

| # | Document |
|---|----------|
| 01 | Software Requirements Specification (SRS) |
| 02 | System Architecture |
| 03 | Database Design |
| 04 | API Specification |
| 05 | UI/UX Specification |
| 06 | User Management Spec |
| 07 | Customer Management Spec |
| 08 | Service Catalog Spec |
| 09 | Order Management Spec |
| 10 | Payment & Receipt Spec |
| 11 | Pickup & Delivery Spec |
| 12 | Dashboard & Reports Spec |
| 13 | Testing Strategy |
| 14 | Deployment Guide |
| 15 | Security Specification |
| 16 | RBAC Specification |
| 17 | Data Validation Rules |
| 18 | Environment Configuration |

---

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch: `git checkout -b feature/your-feature-name`
3. Run the test suite before committing: `python -m pytest`
4. Commit your changes: `git commit -m "feat: add your feature"`
5. Push to the branch: `git push origin feature/your-feature-name`
6. Open a Pull Request

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).

---

© 2026 KleanFlow Laundry Services — Built with 🐍 Python & Flask.
