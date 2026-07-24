
````markdown
# Coding Standards & Development Guidelines

# KleanFlow Laundry Pickup & Delivery Management System

---

# Document Information

| Field | Value |
|--------|-------|
| Document | Coding Standards & Development Guidelines |
| Version | 1.0 |
| Status | Approved |
| Programming Language | Python 3.13+ |
| Backend Framework | Flask |
| Frontend | HTML5, CSS3, Bootstrap 5, JavaScript |
| Database | MySQL 8 |
| ORM | SQLAlchemy |

---

# Table of Contents

1. Purpose
2. General Principles
3. Python Coding Standards
4. Flask Standards
5. HTML Standards
6. CSS Standards
7. JavaScript Standards
8. Database Standards
9. API Standards
10. Error Handling
11. Logging Standards
12. Security Standards
13. Git Standards
14. Documentation Standards
15. Code Review Checklist
16. Definition of Done

---

# 1. Purpose

This document defines the coding standards that every contributor must follow to ensure the KleanFlow codebase remains:

- Clean
- Consistent
- Readable
- Secure
- Maintainable
- Scalable

---

# 2. General Principles

The project shall follow these software engineering principles:

- Keep It Simple (KISS)
- Don't Repeat Yourself (DRY)
- Separation of Concerns (SoC)
- Single Responsibility Principle (SRP)
- Readability over cleverness
- Explicit is better than implicit

---

# 3. Python Coding Standards

## Python Version

```text
Python 3.13+
```

---

## Style Guide

Follow **PEP 8**.

---

## Maximum Line Length

```text
88 characters
```

---

## Naming Conventions

### Variables

```python
customer_name

order_total

payment_reference
```

---

### Functions

Use snake_case.

```python
create_customer()

calculate_total()

generate_receipt()
```

---

### Classes

Use PascalCase.

```python
CustomerService

OrderRepository

PaymentValidator
```

---

### Constants

Use uppercase.

```python
MAX_LOGIN_ATTEMPTS = 5

DEFAULT_CURRENCY = "GHS"
```

---

## Comments

Write comments only when necessary.

Good

```python
# Calculate remaining customer balance
```

Avoid

```python
# Increment i by 1
i += 1
```

---

## Docstrings

Every public class and function should include a docstring.

Example

```python
def calculate_total(order_items):
    """
    Calculate the total cost of an order.

    Args:
        order_items (list): List of order items.

    Returns:
        Decimal: Total order amount.
    """
```

---

# 4. Flask Standards

Use Flask Blueprints.

Example

```text
auth

customers

orders

payments

reports
```

---

## Routes

Routes should:

- Validate requests.
- Call service methods.
- Return responses.

Routes should **not** contain business logic.

---

## Services

Business rules belong in service classes.

Example

```python
CustomerService

OrderService

PaymentService
```

---

## Models

Models should only represent database structures.

Avoid putting business logic inside models.

---

# 5. HTML Standards

Use semantic HTML.

Examples

```html
<header>

<nav>

<main>

<section>

<footer>
```

Avoid excessive `<div>` nesting.

---

## Forms

Every input shall include:

- Label
- Placeholder (where appropriate)
- Validation message
- Accessible name

---

# 6. CSS Standards

Use one responsibility per stylesheet.

Example

```text
auth.css

dashboard.css

tables.css

forms.css

responsive.css
```

---

## Naming

Use kebab-case.

```css
.customer-card

.order-table

.payment-status
```

---

## Avoid

- Inline styles
- `!important` unless unavoidable
- Duplicate selectors

---

# 7. JavaScript Standards

Use modern JavaScript (ES6+).

Prefer:

```javascript
const

let

arrow functions

template literals
```

Avoid:

```javascript
var
```

---

## File Organization

```text
dashboard.js

customers.js

orders.js

payments.js

reports.js
```

---

## Functions

Keep functions short.

Target:

```text
≤ 30 lines
```

---

# 8. Database Standards

All database access shall use SQLAlchemy ORM.

Avoid raw SQL unless performance requires it.

---

## Primary Keys

Every table uses:

```text
id
```

---

## Foreign Keys

Use descriptive names.

Example

```text
customer_id

order_id

payment_id
```

---

## Monetary Values

Always use:

```text
DECIMAL
```

Never use:

```text
FLOAT
```

---

# 9. API Standards

All APIs shall:

- Use JSON.
- Return consistent responses.
- Use RESTful naming.
- Validate inputs.
- Return proper HTTP status codes.

---

## Endpoint Naming

Good

```text
GET /customers

POST /orders

PUT /services/{id}
```

Avoid

```text
/getCustomers

/updateOrderNow
```

---

# 10. Error Handling

Handle errors gracefully.

Use:

- Validation messages
- Try/except blocks
- Custom error pages
- Transaction rollbacks

Do not expose stack traces to users.

---

# 11. Logging Standards

Log important events:

- Login
- Logout
- Failed login
- Customer creation
- Order creation
- Payment recording
- Settings changes
- System errors

Log format should include:

- Timestamp
- User
- Action
- Result

---

# 12. Security Standards

Passwords:

- Hash using Werkzeug.
- Never store plain text.

Input:

- Validate server-side.
- Sanitize user input.

Sessions:

- Secure cookies.
- Session timeout.

Database:

- SQLAlchemy ORM.
- Parameterized queries only.

Environment:

- Store secrets in `.env`.

---

# 13. Git Standards

## Branches

```text
main

develop

feature/<feature-name>

bugfix/<issue-name>

hotfix/<issue-name>
```

---

## Commit Messages

Format:

```text
type: short description
```

Examples

```text
feat: add customer management

fix: correct payment calculation

docs: update API specification

refactor: simplify order service
```

---

# 14. Documentation Standards

Every module should include:

- Purpose
- Inputs
- Outputs
- Dependencies
- Usage examples (where helpful)

Complex business logic should be documented.

---

# 15. Code Review Checklist

Before merging code, verify:

- Code follows PEP 8.
- No duplicated logic.
- Business logic is in services.
- Routes remain lightweight.
- Database queries are optimized.
- Input validation exists.
- Authorization is enforced.
- Error handling is implemented.
- Documentation is updated.
- Tests pass.

---

# 16. Definition of Done

A feature is complete only when:

- Requirements are implemented.
- Code follows project standards.
- Validation is complete.
- Error handling is implemented.
- Security checks are applied.
- Documentation is updated.
- Tests pass successfully.
- Feature is reviewed and approved.

---

# End of Document
````

The next document is **11_Security_Specification.md**, which will define authentication, authorization, RBAC, session management, password policies, CSRF/XSS/SQL injection protection, file upload security, audit logs, backups, and deployment security. This is one of the most important documents because Antigravity will use it to generate secure code rather than just functional code.
