
# Environment Configuration Document

# KleanFlow Laundry Pickup & Delivery Management System

---

# 1. Purpose

This document defines environment configuration required to run KleanFlow safely.

---

# 2. Environment Types

The system supports:

## Development

Used by developers.

Features:

- Debug enabled
- Local database
- Test data

---

## Testing

Used for QA.

Features:

- Separate database
- Automated tests

---

## Production

Used by customers.

Features:

- Debug disabled
- Secure configuration
- HTTPS enabled

---

# 3. Environment File

Location:

```
.env
```

---

Example:

```env
APP_NAME=KleanFlow

FLASK_ENV=development

SECRET_KEY=

MYSQL_HOST=localhost

MYSQL_PORT=3306

MYSQL_USER=root

MYSQL_PASSWORD=

MYSQL_DATABASE=kleanflow


UPLOAD_FOLDER=uploads


MAIL_SERVER=

MAIL_PORT=

MAIL_USERNAME=

MAIL_PASSWORD=


PAYSTACK_PUBLIC_KEY=

PAYSTACK_SECRET_KEY=
```

---

# 4. Configuration Classes

Structure:

```
config.py
```

---

Development:

```python
DevelopmentConfig
```

---

Testing:

```python
TestingConfig
```

---

Production:

```python
ProductionConfig
```

---

# 5. Required Packages

requirements.txt

Example:

```
Flask

Flask-SQLAlchemy

Flask-Migrate

Flask-Login

Flask-WTF

PyMySQL

python-dotenv

Werkzeug

pytest

gunicorn
```

---

# 6. Database Configuration

Connection format:

```
mysql+pymysql://user:password@host/database
```

Example:

```
mysql+pymysql://root:password@localhost/kleanflow
```

---

# 7. Security Configuration

Production requires:

```
DEBUG=False

TESTING=False

SECRET_KEY=strong_random_value
```

---

# 8. File Storage

Allowed folders:

```
uploads/

logs/

backups/
```

---

# 9. Configuration Checklist

Before running:

- Database created
- Environment variables added
- Dependencies installed
- Migration completed
- Admin account created

---

# End of Document
