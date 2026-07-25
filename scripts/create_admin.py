"""
Admin User Bootstrapping CLI Script for KleanFlow Laundry Management System.

Usage:
  Interactive Mode:
    python scripts/create_admin.py

  CLI Arguments Mode:
    python scripts/create_admin.py --email admin@kleanflow.com --name "Admin User" --phone 0201111111 --password "AdminPass123!"
"""

import sys
import os
import argparse

# Ensure application root directory is on Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app
from app.extensions import db
from app.models.user import User
from app.validators.user_validator import UserValidator


def create_admin(full_name, email, phone_number, password):
    app = create_app()
    with app.app_context():
        # Check if user already exists
        existing_user = User.query.filter_by(email=email.strip().lower()).first()

        if existing_user:
            print(f"User with email '{email}' already exists. Updating role to Administrator and resetting password...")
            existing_user.full_name = full_name
            existing_user.phone_number = phone_number
            existing_user.role = 'Administrator'
            existing_user.status = 'Active'
            existing_user.set_password(password)
            db.session.commit()
            print(f"SUCCESS: Administrator '{email}' has been successfully updated.")
            return True

        # Validate input
        user_data = {
            'full_name': full_name,
            'email': email,
            'phone_number': phone_number,
            'role': 'Administrator',
            'status': 'Active',
            'password': password
        }

        errors = UserValidator.validate_user_creation(user_data)
        if errors:
            print("ERROR: Validation failed:")
            for err in errors:
                print(f"  - {err}")
            return False

        new_admin = User(
            full_name=full_name.strip(),
            email=email.strip().lower(),
            phone_number=phone_number.strip(),
            role='Administrator',
            status='Active'
        )
        new_admin.set_password(password)

        db.session.add(new_admin)
        db.session.commit()

        print(f"SUCCESS: Administrator account '{email}' created successfully.")
        return True


def main():
    parser = argparse.ArgumentParser(description="Create or update Administrator user for KleanFlow.")
    parser.add_argument('--name', help="Administrator full name")
    parser.add_argument('--email', help="Administrator email address")
    parser.add_argument('--phone', help="Administrator phone number")
    parser.add_argument('--password', help="Administrator password")

    args = parser.parse_args()

    if args.email and args.password:
        full_name = args.name or "System Administrator"
        phone_number = args.phone or "0200000000"
        create_admin(full_name, args.email, phone_number, args.password)
    else:
        print("=== KleanFlow Administrator Bootstrap Tool ===")
        full_name = input("Enter Full Name [Default: System Administrator]: ").strip() or "System Administrator"
        email = input("Enter Email Address: ").strip()
        while not email:
            print("Email address is required.")
            email = input("Enter Email Address: ").strip()

        phone_number = input("Enter Phone Number [Default: 0200000000]: ").strip() or "0200000000"
        password = input("Enter Password: ").strip()
        while not password:
            print("Password is required.")
            password = input("Enter Password: ").strip()

        create_admin(full_name, email, phone_number, password)


if __name__ == '__main__':
    main()
