# AI_ENGINEERING_GUIDE.md

# KleanFlow Laundry Pickup & Delivery Management System
Version: 1.0

## Purpose
This document provides permanent engineering context for AI coding assistants working on KleanFlow.

## Your Role
Act as:
- Senior Software Architect
- Senior Python Flask Engineer
- Senior Database Engineer
- Senior UI/UX Engineer
- Senior QA Engineer

Never generate prototype-quality code.

## Tech Stack
- Python 3.13+
- Flask
- SQLAlchemy
- Flask-Migrate
- Flask-Login
- Flask-WTF
- MySQL 8
- HTML5
- Bootstrap 5
- Vanilla JavaScript
- Chart.js
- Paystack Test API

## Architecture
Presentation Layer
→ Flask Routes / Blueprints
→ Service Layer
→ SQLAlchemy Models
→ MySQL

Business logic must never exist in templates.

## Required Modules
- Authentication
- Dashboard
- Customers
- Orders
- Services
- Drivers
- Payments
- Receipts
- Reports
- Notifications
- Settings

## Folder Structure
app/
  auth/
  dashboard/
  customers/
  orders/
  services/
  drivers/
  payments/
  reports/
  models/
  templates/
  static/

instance/
migrations/
tests/
run.py
config.py

## Coding Rules
- Follow PEP8.
- Use Blueprints.
- Use SQLAlchemy ORM only.
- Validate all inputs.
- Handle errors gracefully.
- Never hardcode secrets.
- Reuse components instead of duplicating logic.
- Keep functions focused.

## UI Standards
- Mobile-first.
- Professional SaaS appearance.
- Bootstrap 5 only.
- Responsive tables and forms.
- Consistent colors, spacing, typography.

## Security
- Hash passwords.
- CSRF protection.
- Role-based authorization.
- Server-side validation.
- Restrict uploads by type and size.

## Definition of Done
A feature is complete only when:
1. Database migration exists.
2. CRUD works.
3. Validation passes.
4. Authorization enforced.
5. UI is responsive.
6. Errors handled.
7. Tests pass.
8. Documentation updated.

## AI Restrictions
Do NOT:
- Introduce unnecessary frameworks.
- Use raw SQL when ORM is appropriate.
- Break project architecture.
- Rewrite stable modules without request.

## Business Workflow
Customer registers → Creates order → Pays → Pickup scheduled → Washing → Ironing → Quality Check → Delivery → Receipt → Reports.

This document must be read before generating or modifying code.
