"""
User input validation module for KleanFlow authentication and user management.
"""

import re
from app.repositories.user_repository import UserRepository

# Allowed roles in KleanFlow system
VALID_ROLES = [
    'Manager',
    'Laundry Attendant'
]

# Allowed statuses
VALID_STATUSES = ['Active', 'Inactive']


class UserValidator:
    """Validator class for authentication and user management operations."""

    @staticmethod
    def validate_email_format(email):
        """Verify email format via regex."""
        if not email:
            return False
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(email_regex, email.strip()))

    @staticmethod
    def validate_password_strength(password):
        """
        Validates password complexity requirements.
        """
        errors = []
        if not password or len(password) < 6:
            errors.append("Password must be at least 6 characters long.")
        return errors

    @staticmethod
    def validate_login_input(email, password):
        """Validate login form inputs."""
        errors = []
        if not email or not email.strip():
            errors.append("Email address is required.")
        elif not UserValidator.validate_email_format(email):
            errors.append("Invalid email format.")

        if not password or not password.strip():
            errors.append("Password is required.")

        return errors

    @staticmethod
    def validate_user_creation(data):
        """Validate payload for creating a new user."""
        errors = []
        full_name = data.get('full_name', '').strip()
        email = data.get('email', '').strip()
        phone_number = data.get('phone_number', '').strip() if data.get('phone_number') else None
        password = data.get('password', '')
        role = data.get('role', '').strip()
        status = data.get('status', 'Active').strip()

        if not full_name:
            errors.append("Full name is required.")
        elif len(full_name) > 120:
            errors.append("Full name cannot exceed 120 characters.")

        if not email:
            errors.append("Email address is required.")
        elif not UserValidator.validate_email_format(email):
            errors.append("Please enter a valid email address.")
        elif UserRepository.get_by_email(email):
            errors.append("A user with this email address already exists.")

        if phone_number:
            if UserRepository.get_by_phone(phone_number):
                errors.append("A user with this phone number already exists.")

        password_errors = UserValidator.validate_password_strength(password)
        errors.extend(password_errors)

        if not role or role not in VALID_ROLES:
            errors.append(f"Invalid role. Must be one of: {', '.join(VALID_ROLES)}.")

        if status not in VALID_STATUSES:
            errors.append("Invalid status. Must be Active or Inactive.")

        return errors

    @staticmethod
    def validate_user_update(user_id, data):
        """Validate payload for updating an existing user."""
        errors = []
        existing_user = UserRepository.get_by_id(user_id)
        if not existing_user:
            return ["User not found."]

        full_name = data.get('full_name', '').strip()
        email = data.get('email', '').strip()
        phone_number = data.get('phone_number', '').strip() if data.get('phone_number') else None
        role = data.get('role', '').strip()
        status = data.get('status', '').strip()
        password = data.get('password', '')

        if not full_name:
            errors.append("Full name is required.")
        elif len(full_name) > 120:
            errors.append("Full name cannot exceed 120 characters.")

        if not email:
            errors.append("Email address is required.")
        elif not UserValidator.validate_email_format(email):
            errors.append("Please enter a valid email address.")
        else:
            user_by_email = UserRepository.get_by_email(email)
            if user_by_email and user_by_email.id != user_id:
                errors.append("A user with this email address already exists.")

        if phone_number:
            user_by_phone = UserRepository.get_by_phone(phone_number)
            if user_by_phone and user_by_phone.id != user_id:
                errors.append("A user with this phone number already exists.")

        if password:
            password_errors = UserValidator.validate_password_strength(password)
            errors.extend(password_errors)

        if role and role not in VALID_ROLES:
            errors.append(f"Invalid role. Must be one of: {', '.join(VALID_ROLES)}.")

        if status and status not in VALID_STATUSES:
            errors.append("Invalid status. Must be Active or Inactive.")

        return errors
