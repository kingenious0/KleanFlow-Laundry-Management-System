
````markdown
# Project Structure Document

# KleanFlow Laundry Pickup & Delivery Management System

---

# Document Information

| Field | Value |
|--------|-------|
| Document | Project Structure |
| Version | 1.0 |
| Status | Approved |
| Backend | Python Flask |
| Frontend | HTML5, Bootstrap 5 |
| Database | MySQL 8 |

---

# Table of Contents

1. Project Overview
2. Directory Structure
3. Folder Responsibilities
4. Application Modules
5. Static Assets
6. Templates
7. Configuration Files
8. Development Standards
9. Naming Conventions
10. Import Structure
11. Future Expansion

---

# 1. Project Overview

KleanFlow follows a modular Flask architecture based on Blueprints.

Every major business feature is isolated into its own module to improve maintainability, testing, and scalability.

The project is organized so that new developers can easily understand the codebase.

---

# 2. Complete Directory Structure

```text
kleanflow/
│
├── app/
│   │
│   ├── __init__.py
│   ├── extensions.py
│   ├── config.py
│   │
│   ├── auth/
│   ├── dashboard/
│   ├── customers/
│   ├── services/
│   ├── orders/
│   ├── payments/
│   ├── receipts/
│   ├── pickups/
│   ├── deliveries/
│   ├── reports/
│   ├── users/
│   ├── settings/
│   ├── notifications/
│   │
│   ├── models/
│   ├── services_layer/
│   ├── repositories/
│   ├── validators/
│   ├── middleware/
│   ├── utils/
│   ├── decorators/
│   │
│   ├── templates/
│   ├── static/
│   │
│   └── api/
│
├── migrations/
│
├── tests/
│
├── docs/
│
├── scripts/
│
├── uploads/
│
├── logs/
│
├── instance/
│
├── .env
├── .gitignore
├── requirements.txt
├── run.py
├── README.md
└── LICENSE
```

---

# 3. Folder Responsibilities

## app/

Contains the entire application source code.

---

## auth/

Responsible for:

- Login
- Logout
- Password Management
- Authentication
- Authorization

---

## dashboard/

Responsible for:

- Dashboard statistics
- Charts
- Quick summaries
- Recent activities

---

## customers/

Responsible for:

- Customer CRUD
- Search
- Customer history

---

## services/

Responsible for:

- Laundry services
- Pricing
- Service management

---

## orders/

Responsible for:

- Order creation
- Order processing
- Status updates
- Order history

---

## payments/

Responsible for:

- Payment recording
- Payment history
- Balance calculations

---

## receipts/

Responsible for:

- Receipt generation
- Receipt printing
- PDF export

---

## pickups/

Responsible for:

- Pickup requests
- Pickup scheduling
- Pickup assignments

---

## deliveries/

Responsible for:

- Delivery scheduling
- Rider assignments
- Delivery tracking

---

## reports/

Responsible for:

- Revenue reports
- Sales reports
- Customer reports
- Analytics

---

## users/

Responsible for:

- Employee management
- Roles
- Permissions

---

## settings/

Responsible for:

- Business information
- Receipt settings
- Payment configuration
- Appearance

---

## notifications/

Responsible for:

- Alerts
- Notifications
- Messages

---

# 4. Models Folder

```text
models/

user.py

customer.py

service.py

order.py

order_item.py

payment.py

receipt.py

pickup.py

delivery.py

notification.py

setting.py
```

Each model represents one database table.

---

# 5. Services Layer

Business logic belongs here.

Example:

```text
CustomerService

OrderService

PaymentService

ReceiptService

ReportService
```

Routes should never contain business logic.

---

# 6. Repository Layer

Responsible for database operations.

Example

```text
CustomerRepository

OrderRepository

PaymentRepository
```

Responsibilities

- Create
- Read
- Update
- Delete
- Database Queries

---

# 7. Validators

Contains form validation.

Example

```text
customer_validator.py

payment_validator.py

order_validator.py
```

Responsibilities

- Validate inputs
- Return validation errors
- Prevent invalid data

---

# 8. Middleware

Contains reusable request handlers.

Examples

- Authentication checks
- Logging
- Request timing
- Security headers

---

# 9. Decorators

Contains reusable decorators.

Examples

```python
@login_required

@admin_required

@manager_required

@permission_required
```

---

# 10. Utilities

Contains helper functions.

Examples

```text
Date formatting

Currency formatting

Receipt number generator

Random ID generator

File upload helper
```

---

# 11. API Folder

Future REST API.

Example

```text
api/

customers.py

orders.py

payments.py

reports.py
```

---

# 12. Templates Structure

```text
templates/

base.html

dashboard.html

login.html

404.html

500.html

components/

customers/

orders/

payments/

reports/

services/

receipts/

users/

settings/
```

---

# 13. Static Folder

```text
static/

css/

js/

images/

icons/

fonts/

uploads/
```

---

# 14. CSS Structure

```text
css/

style.css

dashboard.css

tables.css

forms.css

auth.css

responsive.css
```

---

# 15. JavaScript Structure

```text
js/

app.js

dashboard.js

orders.js

customers.js

payments.js

reports.js

charts.js

validation.js
```

---

# 16. Uploads Folder

Stores uploaded files.

Example

```text
Business Logo

Profile Images

Receipt PDFs

Attachments
```

---

# 17. Logs Folder

Stores application logs.

Example

```text
application.log

errors.log

security.log
```

---

# 18. Tests Folder

```text
tests/

test_auth.py

test_customers.py

test_orders.py

test_payments.py

test_reports.py
```

---

# 19. Scripts Folder

Contains maintenance scripts.

Examples

```text
seed_database.py

create_admin.py

reset_database.py

backup_database.py
```

---

# 20. Environment Variables

Stored inside

```text
.env
```

Example

```text
SECRET_KEY=

MYSQL_HOST=

MYSQL_PORT=

MYSQL_USER=

MYSQL_PASSWORD=

MYSQL_DATABASE=

PAYSTACK_PUBLIC_KEY=

PAYSTACK_SECRET_KEY=

MAIL_SERVER=

MAIL_USERNAME=

MAIL_PASSWORD=
```

Never commit the `.env` file.

---

# 21. Naming Conventions

## Python Files

Use snake_case.

Example

```text
customer_service.py

payment_repository.py
```

---

## Classes

Use PascalCase.

Example

```python
CustomerService

PaymentRepository

OrderValidator
```

---

## Functions

Use snake_case.

Example

```python
create_order()

calculate_total()

generate_receipt()
```

---

## Variables

Use descriptive snake_case.

Example

```python
customer_name

total_amount

payment_reference
```

---

# 22. Import Standards

Standard Library

↓

Third-party Packages

↓

Local Modules

Example

```python
import os

from flask import Blueprint

from app.models.customer import Customer
```

---

# 23. Blueprint Registration

All Blueprints are registered in

```python
app/__init__.py
```

Example

```python
app.register_blueprint(auth_bp)

app.register_blueprint(customer_bp)

app.register_blueprint(order_bp)
```

---

# 24. Development Workflow

Feature Development

↓

Create Model

↓

Create Repository

↓

Create Service

↓

Create Validator

↓

Create Routes

↓

Create Templates

↓

Testing

↓

Documentation

---

# 25. Git Branch Strategy

```text
main

develop

feature/auth

feature/customers

feature/orders

feature/payments

feature/reports
```

---

# 26. Coding Philosophy

- Keep modules independent.
- Avoid duplicated logic.
- Keep routes lightweight.
- Write reusable services.
- Prefer readability over clever code.
- Document complex logic.
- Use meaningful names.

---

# 27. Future Expansion

Planned folders:

```text
inventory/

expenses/

branches/

customer_portal/

mobile_api/

analytics/

loyalty/

integrations/
```

---

# End of Document
````
