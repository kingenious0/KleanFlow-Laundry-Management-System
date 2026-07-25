# KleanFlow Laundry Management System — Real-Life Workflow & Complete Feature Guide

**Business Name**: KleanFlow Laundry  
**Address**: Asafo By-Pass, Kumasi, Ghana  
**Phone**: +233 55 375 1016 | **Email**: support@kleanflow.com  
**Currency**: Ghanaian Cedi (`GH₵`)

---

## 🔄 Real-Life Operational Workflow (Step-by-Step)

```
[1. Customer Intake] ➔ [2. Order Creation] ➔ [3. Pickup (Optional)] ➔ [4. Laundry Processing] ➔ [5. Payment Recording] ➔ [6. Receipt & Pickup] ➔ [7. Delivery (Optional)]
```

### Stage 1: Customer Drop-off / Intake
1. A customer (e.g. **Kofi Nti Emmanuel**, Phone: `0244447440`) arrives at the Asafo laundry counter or calls for pickup.
2. The Cashier searches for the customer under **Customers** (`/customers/`).
3. If new, the staff clicks **Add Customer** (`/customers/create`), entering name, phone number, email, and address.
4. The system automatically assigns a permanent customer code (e.g., `CUST-100284`).

### Stage 2: Order Creation & Item Pricing
1. The Cashier clicks **Create New Order** (`/orders/create`) and selects `CUST-100284 - Kofi Nti Emmanuel`.
2. The Cashier selects services and quantities:
   - 2x Suit Dry Cleaning (`GH₵ 60.00` each = `GH₵ 120.00`)
   - 1x Heavy Blanket Wash (`GH₵ 40.00` = `GH₵ 40.00`)
3. The system automatically calculates:
   - **Total Amount**: `GH₵ 160.00`
   - **Remaining Balance**: `GH₵ 160.00`
   - **Payment Status**: `Unpaid`
   - **Order Status**: `Pending`
4. The system generates Order Reference `#KF-2026-00001`.

### Stage 3: Pickup Logistics (Optional Home Collection)
1. If the customer requested home pickup, staff navigates to **Logistics ➔ Pickups** (`/logistics/pickups`).
2. Staff clicks **Schedule Pickup**, selects Order `#KF-2026-00001`, sets scheduled date/time, and assigns a driver (`Staff` role).
3. The assigned driver updates status as the task progresses: `Scheduled` ➔ `In Transit` ➔ `Completed`.

### Stage 4: Laundry Processing Lifecycle
The laundry workshop processes the clothes through 6 trackable stages:
1. **Pending** ➔ Items received at facility counter (Mark as **Received**).
2. **Received** ➔ Moved to washing machines (Mark as **Washing**).
3. **Washing** ➔ Moved to dryers & steam ironing station (Mark as **Ironing**).
4. **Ironing** ➔ Quality checked, folded, and packaged (Mark as **Ready**).
5. Customer is notified that clothes are ready for collection.

### Stage 5: Payment Recording
1. Customer pays at the counter or via Mobile Money.
2. Cashier navigates to **Payments ➔ Record Payment** (`/payments/record`) or clicks **Record Payment** directly from the Order Details page.
3. System loads Order `#KF-2026-00001` showing **Balance Due: GH₵ 160.00**.
4. Cashier enters:
   - **Amount**: `160.00` (or `80.00` for partial deposit)
   - **Method**: Selects `Mobile Money` (MTN MoMo) or `Cash`.
5. Cashier clicks **Submit Payment**.
6. System automatically updates:
   - Remaining Balance to `GH₵ 0.00`.
   - Payment Status to **`Paid`** (or **`Partially Paid`** if partial).
   - Order Status to **`Completed`**.

### Stage 6: Receipt Generation & Handover
1. The system automatically generates official receipt `#REC-2026-00001` with reference `#PAY-2026-00001`.
2. Receipt displays KleanFlow Laundry branding (Asafo By-Pass, Kumasi, +233 55 375 1016).
3. Staff prints the receipt or exports PDF for the customer (`/receipts/1/print`).
4. Packaged clothes are handed over to the customer.

### Stage 7: Home Delivery (Optional Final Stage)
1. If delivery was requested, staff schedules a Delivery under **Logistics ➔ Deliveries** (`/logistics/deliveries`).
2. Driver delivers items to customer address and updates status to **Completed**.

---

## 🛡️ User Roles & Access Control Matrix (RBAC)

| Feature / Module | Administrator | Manager | Cashier | Staff |
| :--- | :---: | :---: | :---: | :---: |
| **User Management** | ✅ Full Access | ❌ Read Only | ❌ No Access | ❌ No Access |
| **Customer CRUD** | ✅ Full Access | ✅ Full Access | ✅ Full Access | 👁️ View Only |
| **Service Catalog** | ✅ Full Access | ✅ Full Access | 👁️ View Only | 👁️ View Only |
| **Order Creation & Status** | ✅ Full Access | ✅ Full Access | ✅ Full Access | 👁️ View Only |
| **Payment Recording** | ✅ Full Access | ✅ Full Access | ✅ Full Access | ❌ No Access |
| **Receipt Printing & PDF** | ✅ Full Access | ✅ Full Access | ✅ Full Access | ❌ No Access |
| **Pickups & Deliveries** | ✅ Full Access | ✅ Full Access | ✅ Full Access | ✅ Assigned Tasks Only |
| **Reports & Financial Export** | ✅ Full Access | ✅ Full Access | ❌ No Access | ❌ No Access |

---

## 🧰 Complete Built Feature Inventory

### 1. Authentication & Security
- **Secure Password Hashing**: Uses `Werkzeug` PBKDF2:SHA256 password hashing.
- **Role Guard Decorator**: Custom `@roles_required()` enforcing route boundaries.
- **Session Management**: `Flask-Login` session cookies (`HttpOnly`, `SameSite=Lax`).
- **CSRF Protection**: `Flask-WTF` CSRF token verification on all POST forms.
- **XSS & SQL Injection Defense**: Parameterized ORM queries via SQLAlchemy & Jinja2 auto-escaping.
- **Admin Bootstrap CLI**: `python scripts/create_admin.py` to create/reset administrator credentials.

### 2. Customer Management
- Automated customer code generation (`CUST-XXXXXX`).
- Search filters (by code, name, or phone number) with pagination.
- Customer Profile Page showing total orders, total spent, and current unpaid balance.

### 3. Service Catalog & Pricing
- Categorized services (Wash & Fold, Dry Cleaning, Ironing Only).
- Prices formatted in Ghanaian Cedi (`GH₵`).
- Enable/Disable status toggle to activate or deactivate services.

### 4. Order Processing Engine
- Multi-item order creation with real-time total and balance computation.
- Sequential reference generator (`KF-YYYY-XXXXX`).
- 6-Stage stepper pipeline (`Pending` ➔ `Received` ➔ `Washing` ➔ `Ironing` ➔ `Ready` ➔ `Completed`).
- Order cancellation guard preventing payments/edits on cancelled orders.

### 5. Monetary Payments & Printable Receipts
- Multiple payment methods: Cash, Mobile Money (MTN MoMo/Telecel/AT), Card, Bank Transfer.
- Automatic balance calculation (`Unpaid` ➔ `Partially Paid` ➔ `Paid`).
- Auto-generated receipts (`REC-YYYY-XXXXX`) with printable view and PDF export capability.
- Customizable business branding: **KleanFlow Laundry**, Asafo By-Pass, Kumasi (+233 55 375 1016).

### 6. Logistics & Deliveries
- Pickup scheduling with address, pickup date/time, notes, and driver assignment.
- Delivery scheduling with recipient name, delivery date/time, and driver assignment.
- Status tracking: `Scheduled` ➔ `In Transit` ➔ `Completed` / `Cancelled`.

### 7. Dashboard & Financial Reports
- Real-time KPIs: Today's Revenue, Monthly Revenue, Active Orders, Unpaid Balance.
- Chart.js 4.4 interactive charts: Revenue Trend line chart, Order Status doughnut chart, Top Services bar chart.
- Comprehensive Revenue & Customer Reports with date range filtering.
- One-click CSV export and print view.

### 8. Testing & Deployment Infrastructure
- **81 Automated Tests**: 100% pass rate across domain validators, security boundaries, and end-to-end integration workflows.
- **WSGI Server Configuration**: Production `gunicorn.conf.py` setup.
- **Database Backup Tool**: `python scripts/backup_db.py` for automated snapshots.
- **One-Touch Deployment**: Automation scripts for Linux/Unix (`scripts/deploy.sh`) and Windows (`scripts/deploy.ps1`).
