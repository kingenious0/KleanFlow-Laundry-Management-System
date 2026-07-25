#!/usr/bin/env python3
"""
KleanFlow Laundry Management System — Production Health Check Script.
Verifies that the application, database, and required directories are healthy.

Usage:
    python scripts/healthcheck.py
    python scripts/healthcheck.py --url http://localhost:5000
"""

import sys
import os
import argparse
from pathlib import Path
from urllib import request, error as url_error

# ── Resolve project root ───────────────────────────────────────────────────────
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

CHECKS_PASSED = []
CHECKS_FAILED = []


def pass_check(name: str, detail: str = ""):
    CHECKS_PASSED.append(name)
    print(f"  ✅ PASS  {name}" + (f" — {detail}" if detail else ""))


def fail_check(name: str, detail: str = ""):
    CHECKS_FAILED.append(name)
    print(f"  ❌ FAIL  {name}" + (f" — {detail}" if detail else ""))


def check_env_file():
    env = PROJECT_ROOT / ".env"
    if env.exists():
        content = env.read_text()
        if "change-this-to-a-secure" in content:
            fail_check(".env SECRET_KEY", "Still using default placeholder — set a real secret key!")
        else:
            pass_check(".env", "File present and SECRET_KEY appears to be set")
    else:
        fail_check(".env", "File missing — copy from .env.example and configure")


def check_directories():
    for d in ["logs", "backups", "uploads"]:
        path = PROJECT_ROOT / d
        if path.exists() and path.is_dir():
            pass_check(f"Directory: {d}/", "exists")
        else:
            fail_check(f"Directory: {d}/", "missing — create it")


def check_database():
    try:
        os.environ.setdefault("FLASK_ENV", "production")
        from dotenv import load_dotenv
        load_dotenv(PROJECT_ROOT / ".env")
        from app import create_app
        from app.extensions import db

        app = create_app()
        with app.app_context():
            result = db.session.execute(db.text("SELECT 1")).scalar()
            if result == 1:
                pass_check("Database connection", "Query OK")
            else:
                fail_check("Database connection", "Unexpected query result")
    except Exception as exc:
        fail_check("Database connection", str(exc))


def check_http(url: str):
    try:
        with request.urlopen(url, timeout=5) as resp:
            if resp.status == 200:
                pass_check(f"HTTP GET {url}", f"Status {resp.status}")
            else:
                fail_check(f"HTTP GET {url}", f"Status {resp.status}")
    except url_error.URLError as exc:
        fail_check(f"HTTP GET {url}", str(exc))


def check_requirements():
    req_file = PROJECT_ROOT / "requirements.txt"
    if req_file.exists():
        pass_check("requirements.txt", "Present")
    else:
        fail_check("requirements.txt", "Missing")

    try:
        import flask
        import sqlalchemy
        import flask_login
        pass_check("Core Python packages", f"Flask {flask.__version__}, SQLAlchemy {sqlalchemy.__version__}")
    except ImportError as exc:
        fail_check("Core Python packages", str(exc))


def main():
    parser = argparse.ArgumentParser(description="KleanFlow Production Health Check")
    parser.add_argument("--url", default="http://127.0.0.1:5000", help="App URL to probe")
    parser.add_argument("--skip-http", action="store_true", help="Skip HTTP connectivity check")
    args = parser.parse_args()

    print()
    print("=" * 55)
    print("  KleanFlow — Production Health Check")
    print("=" * 55)
    print()

    check_env_file()
    check_directories()
    check_requirements()
    check_database()

    if not args.skip_http:
        check_http(args.url)

    print()
    print("─" * 55)
    total = len(CHECKS_PASSED) + len(CHECKS_FAILED)
    print(f"  Results: {len(CHECKS_PASSED)}/{total} checks passed")
    if CHECKS_FAILED:
        print()
        print("  Failed checks:")
        for name in CHECKS_FAILED:
            print(f"    • {name}")
        print()
        sys.exit(1)
    else:
        print()
        print("  🎉 All checks passed — application is healthy!")
        print()
        sys.exit(0)


if __name__ == "__main__":
    main()
