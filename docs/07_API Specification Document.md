
````markdown
# API Specification Document

# KleanFlow Laundry Pickup & Delivery Management System

---

# Document Information

| Field | Value |
|--------|-------|
| Document | API Specification |
| Version | 1.0 |
| Status | Approved |
| Architecture | REST API |
| Data Format | JSON |
| Authentication | Flask-Login (Session) / Future JWT |
| Backend | Python Flask |

---

# Table of Contents

1. API Overview
2. Standards
3. Authentication
4. Response Format
5. Error Format
6. Authentication Endpoints
7. Customer API
8. User API
9. Service API
10. Order API
11. Payment API
12. Receipt API
13. Pickup API
14. Delivery API
15. Reports API
16. Dashboard API
17. Notification API
18. Settings API
19. HTTP Status Codes
20. Validation Rules
21. Future API

---

# 1. API Overview

KleanFlow exposes a RESTful API that allows the frontend to communicate with the backend.

Every request shall pass through:

- Authentication
- Authorization
- Validation
- Business Logic
- Database Layer

---

# 2. API Standards

## Base URL

Development

```text
http://localhost:5000/api/v1
```

Production

```text
https://yourdomain.com/api/v1
```

---

## Data Format

All requests and responses use JSON.

Example

```json
{
    "success": true,
    "message": "Customer created successfully."
}
```

---

## Content Type

```text
application/json
```

---

# 3. Authentication

Current

- Flask Login
- Session Authentication

Future

- JWT Authentication
- OAuth Login

---

# 4. Standard Success Response

```json
{
    "success": true,
    "message": "Operation successful.",
    "data": {}
}
```

---

# 5. Standard Error Response

```json
{
    "success": false,
    "message": "Validation failed.",
    "errors": []
}
```

---

# 6. Authentication API

---

## Login

POST

```text
/api/v1/auth/login
```

Body

```json
{
    "email":"admin@example.com",
    "password":"password"
}
```

Response

```json
{
    "success": true,
    "message": "Login successful."
}
```

---

## Logout

POST

```text
/api/v1/auth/logout
```

---

## Current User

GET

```text
/api/v1/auth/me
```

---

## Change Password

PUT

```text
/api/v1/auth/change-password
```

---

# 7. Customer API

---

## Get Customers

GET

```text
/api/v1/customers
```

Returns paginated customers.

---

## Get Customer

GET

```text
/api/v1/customers/{id}
```

---

## Create Customer

POST

```text
/api/v1/customers
```

Body

```json
{
  "full_name":"John Doe",
  "phone_number":"0240000000",
  "email":"john@gmail.com",
  "address":"Kumasi"
}
```

---

## Update Customer

PUT

```text
/api/v1/customers/{id}
```

---

## Delete Customer

DELETE

```text
/api/v1/customers/{id}
```

Soft delete only.

---

## Search Customer

GET

```text
/api/v1/customers/search?query=john
```

---

# 8. User API

---

## Get Users

GET

```text
/api/v1/users
```

---

## Create User

POST

```text
/api/v1/users
```

---

## Update User

PUT

```text
/api/v1/users/{id}
```

---

## Disable User

PATCH

```text
/api/v1/users/{id}/disable
```

---

# 9. Services API

---

## Get Services

GET

```text
/api/v1/services
```

---

## Create Service

POST

```text
/api/v1/services
```

Example

```json
{
"name":"Dry Cleaning",
"price":25
}
```

---

## Update Service

PUT

```text
/api/v1/services/{id}
```

---

## Delete Service

DELETE

```text
/api/v1/services/{id}
```

---

# 10. Orders API

---

## Get Orders

GET

```text
/api/v1/orders
```

---

## Get Order

GET

```text
/api/v1/orders/{id}
```

---

## Create Order

POST

```text
/api/v1/orders
```

Example

```json
{
    "customer_id":1,
    "items":[
        {
            "service_id":2,
            "clothing_type":"Shirt",
            "quantity":4
        }
    ]
}
```

---

## Update Order

PUT

```text
/api/v1/orders/{id}
```

---

## Cancel Order

PATCH

```text
/api/v1/orders/{id}/cancel
```

---

## Update Order Status

PATCH

```text
/api/v1/orders/{id}/status
```

Example

```json
{
    "status":"Ironing"
}
```

---

# 11. Payments API

---

## Get Payments

GET

```text
/api/v1/payments
```

---

## Record Payment

POST

```text
/api/v1/payments
```

Example

```json
{
    "order_id":5,
    "payment_method":"Cash",
    "amount":80
}
```

---

## Payment History

GET

```text
/api/v1/payments/history
```

---

## Verify Payment

POST

```text
/api/v1/payments/verify
```

Future Paystack endpoint.

---

# 12. Receipt API

---

## Generate Receipt

POST

```text
/api/v1/receipts
```

---

## View Receipt

GET

```text
/api/v1/receipts/{id}
```

---

## Print Receipt

GET

```text
/api/v1/receipts/{id}/print
```

---

## Download PDF

GET

```text
/api/v1/receipts/{id}/pdf
```

---

# 13. Pickup API

---

## View Pickup Requests

GET

```text
/api/v1/pickups
```

---

## Create Pickup

POST

```text
/api/v1/pickups
```

---

## Assign Pickup Staff

PATCH

```text
/api/v1/pickups/{id}/assign
```

---

## Update Pickup Status

PATCH

```text
/api/v1/pickups/{id}/status
```

---

# 14. Delivery API

---

## Get Deliveries

GET

```text
/api/v1/deliveries
```

---

## Assign Delivery

PATCH

```text
/api/v1/deliveries/{id}/assign
```

---

## Update Delivery Status

PATCH

```text
/api/v1/deliveries/{id}/status
```

---

## Delivery History

GET

```text
/api/v1/deliveries/history
```

---

# 15. Reports API

---

## Dashboard Report

GET

```text
/api/v1/reports/dashboard
```

---

## Daily Sales

GET

```text
/api/v1/reports/daily-sales
```

---

## Monthly Sales

GET

```text
/api/v1/reports/monthly-sales
```

---

## Customer Report

GET

```text
/api/v1/reports/customers
```

---

## Revenue Report

GET

```text
/api/v1/reports/revenue
```

---

# 16. Dashboard API

---

## Dashboard Statistics

GET

```text
/api/v1/dashboard
```

Returns

```json
{
    "customers":500,
    "orders":120,
    "revenue":25000,
    "pending_orders":15
}
```

---

# 17. Notification API

---

## Get Notifications

GET

```text
/api/v1/notifications
```

---

## Mark Read

PATCH

```text
/api/v1/notifications/{id}/read
```

---

## Delete Notification

DELETE

```text
/api/v1/notifications/{id}
```

---

# 18. Settings API

---

## Get Settings

GET

```text
/api/v1/settings
```

---

## Update Settings

PUT

```text
/api/v1/settings
```

---

# 19. HTTP Status Codes

| Code | Meaning |
|-------|----------|
|200|Success|
|201|Created|
|204|No Content|
|400|Bad Request|
|401|Unauthorized|
|403|Forbidden|
|404|Not Found|
|409|Conflict|
|422|Validation Error|
|500|Internal Server Error|

---

# 20. Validation Rules

## Customer

- Name required
- Phone required
- Phone unique

---

## Service

- Name required
- Price required
- Price > 0

---

## Order

- Customer required
- Minimum one item
- Quantity > 0

---

## Payment

- Amount > 0
- Valid payment method
- Cannot exceed order balance

---

# 21. Security Requirements

Every endpoint shall:

- Require authentication.
- Validate permissions.
- Sanitize inputs.
- Return standardized responses.
- Prevent SQL Injection using SQLAlchemy.
- Log sensitive operations.

---

# 22. Versioning Strategy

Current Version

```text
/api/v1/
```

Future

```text
/api/v2/
```

```text
/api/v3/
```

Old versions should remain supported until officially deprecated.

---

# 23. Future API Endpoints

Future integrations include:

```text
/api/v2/mobile

/api/v2/customer-portal

/api/v2/paystack

/api/v2/loyalty

/api/v2/inventory

/api/v2/expenses

/api/v2/analytics
```

---

# 24. API Development Standards

- Use Flask Blueprints.
- Return JSON consistently.
- Use proper HTTP verbs.
- Keep controllers thin.
- Move business logic into service classes.
- Validate all incoming data.
- Document every endpoint.
- Write tests for every endpoint.

---

# End of Document
````
