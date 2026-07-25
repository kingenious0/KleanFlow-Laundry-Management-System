# Changelog

All notable changes to KleanFlow Laundry Management System are documented here.
This project adheres to [Semantic Versioning](https://semver.org/).

---

## [1.0.0] — 2026-07-25

### 🎉 Initial Production Release

#### ✅ Core Features Added
- **User Management & RBAC** — 4-role system (Administrator, Manager, Cashier, Staff) with full CRUD and role-based route guards
- **Authentication** — Email/password login with session management, inactive account blocking, and CSRF protection
- **Customer Management** — Auto-generated `CUST-XXXXXX` codes, full profile management, search/filter/pagination, order history view
- **Service Catalog** — Categorized services with GH₵ pricing, enable/disable, and soft-delete
- **Order Management** — Multi-item order creation with real-time totals, 6-stage lifecycle workflow (Pending → Received → Washing → Ironing → Ready → Completed / Cancelled)
- **Payment & Receipts** — Multiple payment methods (Cash, Mobile Money, Card, Bank Transfer), partial payment support, automatic balance tracking, receipt generation (`REC-YYYY-XXXXX`) with printable format
- **Pickup & Delivery** — Schedule pickup and delivery logistics, assign Staff drivers, track status (Scheduled → In Transit → Completed / Cancelled)
- **Dashboard** — Real-time KPIs (Today's Revenue, Monthly Revenue, Active Orders, Unpaid Balance), Chart.js revenue trend, order status breakdown, top services charts
- **Reports** — Filtered Revenue Report and Customer Report with CSV export
- **PDF Export** — Printable receipt and order report templates

#### 🔒 Security
- CSRF protection on all forms via Flask-WTF
- XSS prevention via Jinja2 auto-escaping
- SQL injection prevention via SQLAlchemy parameterized queries
- Password hashing with Werkzeug `pbkdf2:sha256`
- Role-based route access control enforced at every blueprint endpoint
- `SESSION_COOKIE_SECURE`, `SESSION_COOKIE_HTTPONLY`, `SESSION_COOKIE_SAMESITE` hardened

#### 🧪 Testing
- 81 automated tests across 11 test modules
- Unit, integration, security, and full end-to-end business lifecycle tests
- pytest with SQLite in-memory test isolation

#### 📦 Deployment
- Gunicorn WSGI production server configuration
- Linux deployment script (`scripts/deploy.sh`)
- Windows deployment script (`scripts/deploy.ps1`)
- Nginx reverse proxy configuration (`scripts/nginx.conf`)
- Systemd service unit file (`scripts/kleanflow.service`)
- Database backup utility (`scripts/backup_db.py`)
- Comprehensive `.env.example` environment template

#### 📚 Documentation
- 18 specification and design documents in `docs/`
- Complete architecture, SRS, API spec, UI/UX spec, deployment guide, security spec

---

## [Unreleased]

### Planned
- Email notifications for order status changes
- Customer-facing self-service portal
- WhatsApp order status updates (via Twilio or local provider)
- Mobile-responsive PWA improvements
- Multi-branch support
