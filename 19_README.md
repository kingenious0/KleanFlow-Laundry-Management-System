
# README.md

# KleanFlow Laundry Pickup & Delivery Management System

---

# Overview

KleanFlow is a web-based laundry management system designed to help small and medium laundry businesses manage daily operations.

The system provides:

- Customer management
- Laundry order processing
- Payment tracking
- Receipt generation
- Pickup scheduling
- Delivery management
- Business reports

---

# Features

## Authentication

- Secure login
- Role-based access
- Employee management

---

## Customer Management

- Add customers
- Edit information
- View history
- Search customers

---

## Order Management

- Create laundry orders
- Track progress
- Calculate totals
- Manage statuses

---

## Payment Management

- Record payments
- Track balances
- Generate receipts

---

## Delivery Management

- Schedule pickups
- Assign delivery staff
- Track completion

---

## Reports

- Revenue reports
- Sales reports
- Customer statistics

---

# Technology Stack

## Frontend

- HTML5
- CSS3
- Bootstrap 5
- JavaScript

---

## Backend

- Python
- Flask

---

## Database

- MySQL

---

# Installation

## Clone Repository

```bash
git clone repository-url
```

---

## Create Environment

```bash
python -m venv venv
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Configure Database

Create:

```
.env
```

Add database credentials.

---

## Run Migration

```bash
flask db upgrade
```

---

## Start Application

```bash
python run.py
```

---

# Default Roles

## Administrator

Full system access.

## Manager

Business operation management.

## Cashier

Orders and payments.

## Staff

Assigned tasks.

---

# Project Structure

```
app/

models/

templates/

static/

tests/

docs/
```

---

# Development

Create feature branch:

```bash
git checkout -b feature/name
```

Commit:

```bash
git commit -m "feat: add feature"
```

Push:

```bash
git push origin feature/name
```

---

# Testing

Run:

```bash
pytest
```

---

# Deployment

Supported:

- Local server
- VPS
- Render
- Railway
- Cloud platforms

---

# Future Improvements

Planned:

- Customer portal
- Mobile application
- Online payments
- QR receipts
- Inventory management
- Multi-branch support

---

# License

MIT License

---

# Author

KleanFlow Development Team

---

# End of Document
