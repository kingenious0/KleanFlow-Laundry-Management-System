
````markdown
# UI/UX Specification Document

# KleanFlow Laundry Pickup & Delivery Management System

---

# Document Information

| Field | Value |
|--------|-------|
| Document | UI/UX Specification |
| Version | 1.0 |
| Status | Approved |
| Design Style | Modern SaaS Dashboard |
| Framework | Bootstrap 5 |
| Icons | Bootstrap Icons |
| Charts | Chart.js |
| Responsive | Yes |

---

# Table of Contents

1. Design Vision
2. Design Principles
3. Branding
4. Color Palette
5. Typography
6. Spacing System
7. Layout Structure
8. Navigation
9. Dashboard
10. Authentication Screens
11. Customer Module
12. Services Module
13. Orders Module
14. Payments Module
15. Receipts Module
16. Reports Module
17. Settings Module
18. Components
19. Responsive Design
20. Accessibility
21. UX Guidelines
22. Future Improvements

---

# 1. Design Vision

KleanFlow should look like a modern commercial SaaS application rather than a typical student project.

The interface should be:

- Clean
- Professional
- Fast
- Spacious
- Easy to understand
- Mobile friendly
- Minimalistic

Design inspiration:

- Stripe Dashboard
- Notion
- Linear
- Shopify Admin
- Vercel Dashboard

---

# 2. Design Principles

The UI shall follow these principles:

- Simplicity over decoration
- Consistency across pages
- Fast navigation
- Clear hierarchy
- Minimal clicks
- Responsive layouts

---

# 3. Branding

## Logo

Simple laundry-themed icon with modern typography.

Example:

```text
🧺 KleanFlow
```

---

## Brand Personality

- Modern
- Trustworthy
- Clean
- Professional
- Friendly

---

# 4. Color Palette

## Primary

```text
#2563EB
```

Blue

---

## Secondary

```text
#F8FAFC
```

Light Gray

---

## Background

```text
#FFFFFF
```

White

---

## Sidebar

```text
#0F172A
```

Dark Navy

---

## Success

```text
#22C55E
```

---

## Warning

```text
#F59E0B
```

---

## Danger

```text
#EF4444
```

---

## Info

```text
#06B6D4
```

---

# 5. Typography

Font Family

```text
Inter
```

Fallback

```text
Arial

sans-serif
```

---

## Heading Sizes

| Element | Size |
|----------|------|
| H1 | 36px |
| H2 | 30px |
| H3 | 24px |
| H4 | 20px |
| Body | 16px |
| Small | 14px |

---

## Font Weights

```text
400

500

600

700
```

---

# 6. Spacing System

Base spacing

```text
8px
```

Spacing scale

```text
4

8

12

16

24

32

48

64
```

---

# 7. Overall Layout

Desktop Layout

```text
-----------------------------------------

Top Navbar

-----------------------------------------

Sidebar | Main Content

Sidebar | Main Content

Sidebar | Main Content

-----------------------------------------
```

---

# Sidebar Width

```text
260px
```

Collapsed

```text
80px
```

---

# Navbar Height

```text
70px
```

---

# 8. Navigation Structure

```text
Dashboard

Customers

Orders

Services

Payments

Receipts

Pickup

Delivery

Reports

Users

Settings

Logout
```

---

# Sidebar Behavior

Desktop

Permanent sidebar.

Mobile

Collapsible drawer.

---

# 9. Dashboard

Dashboard contains:

---

## Statistic Cards

- Customers
- Orders
- Revenue
- Pending Orders
- Deliveries
- Pickups
- Today's Sales
- Outstanding Balance

---

## Charts

Revenue

```text
Line Chart
```

Orders

```text
Bar Chart
```

Payments

```text
Pie Chart
```

Monthly Revenue

```text
Area Chart
```

---

## Tables

Recent Orders

Recent Payments

Recent Customers

Upcoming Deliveries

---

# 10. Login Page

Components

- Logo
- Welcome message
- Email
- Password
- Remember Me
- Login Button
- Forgot Password

---

Layout

```text
Centered Card

Soft Shadow

Rounded Corners

White Background
```

---

# 11. Dashboard Cards

Each card contains

```text
Icon

Title

Value

Trend Indicator

Small Description
```

Example

```text
📦

Orders

125

↑ 15%

Compared to yesterday
```

---

# 12. Customer Page

Toolbar

- Search
- Filter
- Add Customer

Table

- Name
- Phone
- Address
- Orders
- Status
- Actions

Actions

- View
- Edit
- Delete
- History

---

# 13. Service Page

Cards or table.

Columns

- Service Name
- Price
- Status
- Created Date
- Actions

---

# 14. Orders Page

Top

Filters

- Pending
- Washing
- Ironing
- Ready
- Completed

Search

Date Filter

Customer Filter

---

Table Columns

- Order Number
- Customer
- Total
- Balance
- Status
- Payment
- Actions

---

Status Colors

Pending

Yellow

Washing

Blue

Ironing

Purple

Ready

Green

Completed

Dark Green

Cancelled

Red

---

# 15. Create Order Screen

Step 1

Select Customer

↓

Step 2

Select Services

↓

Step 3

Add Clothing Items

↓

Step 4

Calculate Total

↓

Step 5

Payment

↓

Step 6

Receipt

---

# 16. Payments Page

Cards

Today's Revenue

Pending Payments

Total Payments

Outstanding Balance

---

Table

Reference

Order

Amount

Method

Status

Date

---

# 17. Receipt Screen

Professional printable receipt.

Contains

```text
Business Logo

Receipt Number

Customer

Items

Services

Amount

Payment Method

Cashier

Date

QR Code (Future)
```

---

# 18. Reports Page

Sections

Sales

Customers

Payments

Orders

Revenue

---

Charts

Revenue Trend

Orders

Payments

Monthly Comparison

Customer Growth

---

Export Buttons

PDF

Excel

Print

---

# 19. Settings Page

Cards

Business Profile

Receipt Settings

Payment Settings

Appearance

Security

Users

---

# 20. Buttons

Primary

```text
Blue
```

Secondary

```text
Gray
```

Success

```text
Green
```

Danger

```text
Red
```

Warning

```text
Orange
```

---

# 21. Forms

Every form shall include

- Labels
- Placeholder
- Validation
- Error Message
- Help Text

---

Input Height

```text
48px
```

Border Radius

```text
12px
```

---

# 22. Tables

Tables shall support

- Pagination
- Search
- Sorting
- Filtering
- Row Selection

---

# 23. Modal Windows

Use modals for

- Delete Confirmation
- Quick View
- Payment Confirmation
- Status Update

---

# 24. Notifications

Notification Bell

Dropdown

Unread Counter

Types

Success

Info

Warning

Error

---

# 25. Loading States

Use

- Skeleton loaders
- Spinner
- Progress bars

Never leave blank screens.

---

# 26. Empty States

Every empty page shall include

- Illustration
- Helpful message
- Action button

Example

```text
No Orders Yet

Create your first laundry order.
```

---

# 27. Responsive Design

Desktop

≥1200px

---

Tablet

768px–1199px

---

Mobile

<768px

---

Mobile Features

- Drawer Sidebar
- Responsive Tables
- Stacked Cards
- Large Buttons

---

# 28. Accessibility

Support

- Keyboard Navigation
- Screen Readers
- High Contrast
- Visible Focus States

---

# 29. Micro Interactions

Use animations for

- Button Hover
- Card Hover
- Sidebar Collapse
- Success Messages
- Modal Opening

Animation duration

```text
0.2s
```

---

# 30. Icons

Use Bootstrap Icons.

Examples

```text
bi-house

bi-person

bi-basket

bi-receipt

bi-cash

bi-truck

bi-gear

bi-graph-up

bi-box
```

---

# 31. Dark Mode

Future support

Dark sidebar

Dark cards

Dark tables

Dark charts

Theme switcher

---

# 32. UX Principles

Users should complete common tasks quickly.

Examples

Register Customer

≤30 seconds

Create Order

≤2 minutes

Receive Payment

≤30 seconds

Print Receipt

≤10 seconds

---

# 33. Future UI Enhancements

- Multi-language support
- Theme customization
- Drag-and-drop dashboard widgets
- Customer self-service portal
- Progressive Web App (PWA)
- Offline support
- QR code receipt verification
- Real-time notifications

---

# End of Document
````

### **Next document (recommended):**

`09_Project_Structure.md`

After that we'll do:

10. Coding Standards
11. Security Specification
12. Development Roadmap
13. Testing Strategy
14. Deployment Guide
15. User Manual
16. Business Rules
17. Environment Configuration
18. CONTRIBUTING.md
19. CHANGELOG.md
20. README.md

These remaining documents will complete a professional, GitHub-ready documentation package for KleanFlow.
