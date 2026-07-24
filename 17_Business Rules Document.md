
# Business Rules Document

# KleanFlow Laundry Pickup & Delivery Management System

---

# 1. Overview

This document defines the operational rules that control how KleanFlow behaves.

Business rules ensure that the system follows real laundry business processes.

---

# 2. Customer Rules

## BR-CUS-001: Customer Registration

A customer must provide:

- Full name
- Phone number
- Address

before registration is completed.

---

## BR-CUS-002: Unique Customer Identity

A phone number should belong to only one active customer.

Duplicate customers should be prevented.

---

## BR-CUS-003: Customer History

All customer orders and payments must remain connected to the customer profile.

---

# 3. Service Rules

## BR-SER-001: Service Creation

Every service must have:

- Service name
- Description
- Price
- Status

---

## BR-SER-002: Service Availability

Only active services can be selected when creating orders.

---

## BR-SER-003: Price Management

Changing a service price affects future orders only.

Existing orders keep their original price.

---

# 4. Order Rules

## BR-ORD-001: Order Creation

An order requires:

- Customer
- At least one service item
- Quantity
- Date

---

## BR-ORD-002: Order Number

Every order must have a unique reference number.

Example:

```
KF-2026-00001
```

---

## BR-ORD-003: Order Status Flow

Allowed workflow:

```
Pending

↓

Received

↓

Washing

↓

Ironing

↓

Ready

↓

Completed
```

---

## BR-ORD-004: Cancellation

Cancelled orders:

- Cannot receive new payments.
- Remain in history.
- Cannot be deleted permanently.

---

# 5. Payment Rules

## BR-PAY-001: Payment Recording

Every payment must belong to an existing order.

---

## BR-PAY-002: Payment Amount

Payment amount must:

- Be greater than zero.
- Not exceed remaining balance.

---

## BR-PAY-003: Payment Status

Order payment status:

```
Unpaid

Partially Paid

Paid
```

---

# 6. Receipt Rules

## BR-REC-001

Every successful payment generates a receipt.

---

## BR-REC-002

Receipt must contain:

- Business details
- Customer information
- Order details
- Payment information
- Date

---

# 7. Pickup Rules

Pickup requires:

- Customer address
- Pickup date
- Assigned staff

---

# 8. Delivery Rules

Delivery can only happen when:

Order status:

```
Ready
```

---

# 9. User Management Rules

## Administrator

Can:

- Manage users
- Change settings
- View all reports

---

## Manager

Can:

- Manage operations
- View reports

---

## Cashier

Can:

- Create orders
- Receive payments
- Print receipts

---

## Staff

Can:

- Update assigned tasks

---

# 10. Data Integrity Rules

The system must prevent:

- Invalid orders
- Negative payments
- Duplicate receipts
- Missing customers
- Broken relationships

---

# 11. Reporting Rules

Reports must calculate:

Revenue:

```
Sum of completed payments
```

Outstanding balance:

```
Order Total - Payments
```

---

# End of Document
