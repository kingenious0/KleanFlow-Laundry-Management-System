# KleanFlow Laundry Pickup & Delivery Management System
## Project Constitution
**Version:** 1.0
**Status:** Approved
**Project Type:** Commercial SaaS-inspired Business Management System
**Technology Stack:** Python Flask + MySQL + Bootstrap 5

---

# 1. Purpose

This Constitution establishes the guiding principles, engineering standards, architectural rules, development philosophy, and quality expectations for the KleanFlow Laundry Pickup & Delivery Management System.

All contributors—including software developers, AI coding assistants, designers, testers, and maintainers—must follow this document throughout the lifecycle of the project.

This document serves as the highest-level authority for all technical and product decisions.

---

# 2. Vision Statement

KleanFlow aims to digitize and simplify the operations of small and medium-sized laundry businesses by providing an intuitive, secure, scalable, and modern web-based management platform.

The application should resemble a real commercial SaaS product while remaining deployable as a standalone application for demonstration or self-hosting.

---

# 3. Mission

To provide laundry businesses with an affordable digital solution that replaces manual record-keeping, improves operational efficiency, enhances customer experience, and provides meaningful business insights.

---

# 4. Product Philosophy

KleanFlow must always be:

- Simple to understand.
- Easy to operate.
- Fast to use.
- Secure.
- Professional.
- Responsive.
- Reliable.
- Maintainable.
- Modular.
- Extensible.

Every feature must solve a genuine business problem.

Features that do not provide measurable business value should not be included in the MVP.

---

# 5. Development Principles

- Readability over cleverness.
- Maintainability over shortcuts.
- Reusability over duplication.
- Simplicity over unnecessary complexity.
- Business value over technical novelty.

---

# 6. Core Engineering Principles

- Separate business logic from presentation.
- Build modular features.
- Follow the Single Responsibility Principle.
- Avoid duplicated code (DRY).
- Store configuration in environment variables.

---

# 7. Technology Standards

## Backend
- Python 3.13+
- Flask
- SQLAlchemy
- Flask-Migrate
- Flask-Login
- Flask-WTF

## Database
- MySQL 8+

## Frontend
- HTML5
- CSS3
- Bootstrap 5
- Vanilla JavaScript
- Chart.js
- Bootstrap Icons

---

# 8. User Experience Principles

- Commercial-quality interface.
- Mobile-first and responsive.
- Simple navigation.
- Consistent design.

---

# 9. Security Principles

- Hash passwords.
- Validate all inputs.
- Use SQLAlchemy ORM.
- Enable CSRF protection.
- Never expose secrets.
- Enforce role-based authorization.

---

# 10. Database Principles

- Primary keys
- Foreign keys
- Timestamps
- Normalized schema
- Meaningful naming

---

# 11. Coding Standards

- Follow PEP 8.
- Small functions.
- Meaningful names.
- Reusable code.
- Comments explain why, not what.

---

# 12. Business Rules

- Paid orders proceed automatically.
- Completed orders cannot be edited.
- Receipts are immutable.
- Every payment has a unique reference.

---

# 13. Performance Objectives

- Fast page loads.
- Optimized queries.
- Pagination for large tables.

---

# 14. Accessibility

- Proper labels.
- Keyboard-friendly navigation.
- Responsive layouts.

---

# 15. Logging

Log:
- Authentication events
- Payments
- Order changes
- Administrative actions
- Errors

---

# 16. Error Handling

- Friendly error messages.
- Log unexpected exceptions.
- Never show stack traces to users.

---

# 17. AI Development Policy

AI assistants must:
- Read documentation first.
- Follow project architecture.
- Avoid unnecessary dependencies.
- Produce production-quality code.

---

# 18. MVP Scope

- Authentication
- Role-Based Access
- Customer Management
- Laundry Orders
- Services
- Payments
- Receipts
- Reports
- Dashboard
- Settings

---

# 19. Success Criteria

- Complete business workflow.
- Accurate reports.
- Secure authentication.
- Reliable payment verification.
- Professional architecture.

---

# 20. Guiding Principle

Choose solutions that are easier to understand, maintain, test, and extend.
