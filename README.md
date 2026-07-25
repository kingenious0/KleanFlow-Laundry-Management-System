# KleanFlow — Laundry Pickup & Delivery Management System

[![Build Status](https://img.shields.io/badge/tests-81%20passed-brightgreen.svg)](https://github.com/kingenious0/KleanFlow-Laundry-Management-System)
[![Python Version](https://img.shields.io/badge/python-3.13%20%7C%203.14-blue.svg)](https://www.python.org/)
[![Framework](https://img.shields.io/badge/framework-Flask%203.1-black.svg)](https://flask.palletsprojects.org/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

KleanFlow is a web-based laundry management system designed for small and medium-sized laundry and dry cleaning businesses in Ghana. It streamlines end-to-end operational workflows including user management with Role-Based Access Control (RBAC), customer management, laundry service catalogs, order creation, payment recording with automatic receipt generation (in Ghanaian Cedi `GH₵`), pickup & delivery logistics scheduling, business intelligence dashboards, financial reporting, and PDF exports.

---

## 🌟 Key Features

### 🔐 1. User Management & Security
- **Role-Based Access Control (RBAC)**: Supports `Administrator`, `Manager`, `Cashier`, and `Staff` roles.
- **Authentication**: Password hashing via `Werkzeug`, session protection with `Flask-Login`, CSRF protection with `Flask-WTF`, auto-escaping against XSS, and parameterized queries against SQL injection.
- **Self-Service Profile**: User password change and details update.

### 👥 2. Customer Management
- Automated customer code generation (`CUST-XXXXXX`).
- Search by customer code, name, or phone number with pagination.
- Complete customer profile with order history and balance tracking.

### 🧺 3. Laundry Service Catalog
- Service categories (e.g., Wash & Fold, Dry Cleaning, Ironing Only).
- Pricing in Ghanaian Cedi (`GH₵`), status enabling/disabling, and input validation.

### 📋 4. Laundry Order Workflow
- Multi-item order creation with real-time total and balance computation.
- Automatic order number generation (`ORD-YYYY-XXXXX`).
- 6-Stage Order Lifecycle: `Pending` ➔ `Received` ➔ `Washing` ➔ `Ironing` ➔ `Ready` ➔ `Completed` / `Cancelled`.

### 💳 5. Payments & Receipts
- Multiple payment methods: `Cash`, `Mobile Money`, `Card`, `Bank Transfer`.
- Balance tracking with automatic payment status (`Unpaid`, `Partially Paid`, `Paid`).
- Automatic receipt generation (`REC-YYYY-XXXXX`) with printable format and PDF export capability.

### 🚚 6. Pickup & Delivery Scheduling
- Pickup and delivery scheduling with driver assignment (`Staff` role filtering).
- Status tracking (`Scheduled`, `In Transit`, `Completed`, `Cancelled`).

### 📊 7. Dashboard & Financial Reports
- Real-time KPIs: Today's Revenue, Monthly Revenue, Active Orders, Unpaid Balance.
- Interactive Chart.js visualisations: Revenue trends, Order Status Breakdown, Top Services.
- Detailed Revenue Reports & Customer Financial Reports with CSV export.

---

## 🛠️ Technology Stack

- **Backend**: Python 3.13+, Flask 3.1+, SQLAlchemy 2.0+ (ORM), Flask-Migrate, Flask-Login, Flask-WTF.
- **Frontend**: HTML5, Vanilla CSS, Bootstrap 5.3, Chart.js 4.4, Remix Icon set.
- **Database**: MySQL 8.0+ (Production) / SQLite (Development & Testing).
- **WSGI Server**: Gunicorn 23.0+.
- **Testing**: pytest 9.1+, HTML/JSON test suite reporting.

---

## 🚀 Quick Start Guide

### Prerequisites
- Python 3.13 or higher
- MySQL 8.0+ (optional for local testing; SQLite works out-of-the-box)
- Git

### 1. Clone Repository
```bash
git clone https://github.com/kingenious0/KleanFlow-Laundry-Management-System.git
cd "KleanFlow Laundry Management System"
```

### 2. Create Virtual Environment & Install Dependencies
**Linux / macOS:**
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

**Windows:**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### 3. Environment Setup
Copy the example environment configuration:
```bash
cp .env.example .env
```
Edit `.env` to configure your database connection and secret key.

### 4. Database Migration & Admin Creation
Run database migrations and bootstrap the initial Administrator user:
```bash
flask db upgrade
python scripts/create_admin.py --email admin@kleanflow.com --name "System Administrator" --phone 0200000000 --password "AdminPass123!"
```

### 5. Run Local Development Server
```bash
python run.py
```
Open `http://localhost:5000` in your web browser and login with `admin@kleanflow.com` / `AdminPass123!`.

---

## 🧪 Running Automated Tests

KleanFlow includes a comprehensive 81-test suite covering domain validation, security boundaries, and full end-to-end integration workflows:

```bash
python -m pytest
```

To run individual test files:
```bash
python -m pytest tests/test_security.py
python -m pytest tests/test_integration_workflows.py
```

---

## 📦 Production Deployment

Automated deployment scripts are provided for both Linux and Windows environments:

### Linux / Unix (Nginx + Gunicorn)
```bash
chmod +x scripts/deploy.sh
./scripts/deploy.sh
```

### Windows Server (PowerShell)
```powershell
.\scripts\deploy.ps1
```

### Database Backup
Run daily database snapshots:
```bash
python scripts/backup_db.py
```

---

## 📂 Project Architecture

```
├── app/
│   ├── auth/                # Authentication Blueprint & Routes
│   ├── blueprints/          # Feature Blueprints (users, customers, services, orders, payments, logistics, reports, dashboard)
│   ├── models/              # SQLAlchemy Database Models
│   ├── repositories/        # Data Access Layer (Repository Pattern)
│   ├── services_layer/      # Core Business Logic Layer
│   ├── static/              # Static Assets (CSS, JS, Images)
│   ├── templates/           # Jinja2 HTML Templates
│   ├── validators/          # Input & Business Rule Validation Layer
│   ├── config.py            # App Configurations (Dev, Test, Prod)
│   └── extensions.py        # Flask Extensions Initialisation
├── docs/                    # Complete Architecture & SRS Specifications
├── scripts/                 # Admin creation, database backup, & deployment scripts
├── tests/                   # Pytest Test Suites (81 tests)
├── gunicorn.conf.py         # Production WSGI Server Configuration
├── run.py                   # Application Entry Point
└── requirements.txt         # Project Dependencies
```

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).

---

© 2026 KleanFlow Laundry Services — Built with Python & Flask.
