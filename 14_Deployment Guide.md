
# Deployment Guide

# KleanFlow Laundry Pickup & Delivery Management System

---

# 1. Overview

This document explains how to install, configure, run, and deploy KleanFlow.

The system supports:

- Local development
- Testing environment
- Production deployment

---

# 2. Technology Requirements

## Required Software

Install:

- Python 3.13+
- MySQL 8+
- Git
- Code Editor
- Web Browser

Recommended:

- VS Code
- Antigravity IDE
- Google Chrome

---

# 3. Clone Repository

```bash
git clone https://github.com/username/kleanflow.git
```

Move into project:

```bash
cd kleanflow
```

---

# 4. Create Virtual Environment

Windows:

```bash
python -m venv venv
```

Activate:

```bash
venv\Scripts\activate
```

Linux/Mac:

```bash
source venv/bin/activate
```

---

# 5. Install Dependencies

```bash
pip install -r requirements.txt
```

---

# 6. Environment Configuration

Create:

```
.env
```

Example:

```env
SECRET_KEY=your_secret_key

MYSQL_HOST=localhost

MYSQL_PORT=3306

MYSQL_USER=root

MYSQL_PASSWORD=password

MYSQL_DATABASE=kleanflow

FLASK_ENV=development
```

---

# 7. Database Setup

Create database:

```sql
CREATE DATABASE kleanflow;
```

Run migrations:

```bash
flask db upgrade
```

---

# 8. Create Admin Account

Run:

```bash
python scripts/create_admin.py
```

Example:

```
Email:
admin@kleanflow.com

Password:
Admin@123
```

---

# 9. Run Application

Development:

```bash
python run.py
```

Application:

```
http://localhost:5000
```

---

# 10. Production Deployment

Recommended stack:

```
Nginx

↓

Gunicorn

↓

Flask Application

↓

MySQL Database
```

---

# 11. Production Checklist

Before deployment:

- Disable debug mode
- Configure HTTPS
- Secure environment variables
- Create database backup
- Configure logging
- Test authentication

---

# 12. Backup Strategy

Daily:

- Database backup

Weekly:

- Full project backup

Monthly:

- Archive backup

---

# End of Document
