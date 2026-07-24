"""
Customer input validation module for KleanFlow customer management.
"""

import re
from app.repositories.customer_repository import CustomerRepository


class CustomerValidator:
    """Validator class for customer management operations."""

    @staticmethod
    def validate_email_format(email):
        """Verify email format via regex."""
        if not email:
            return True  # Optional field
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(email_regex, email.strip()))

    @staticmethod
    def validate_phone_format(phone):
        """Verify phone number length and basic numeric/plus format."""
        if not phone:
            return False
        clean_phone = phone.strip()
        # Allows digits, spaces, hyphens, and leading plus
        phone_regex = r'^\+?[0-9\s\-]{7,20}$'
        return bool(re.match(phone_regex, clean_phone))

    @staticmethod
    def validate_customer_creation(data):
        """Validate payload for registering a new customer (BR-CUS-001 & BR-CUS-002)."""
        errors = []
        full_name = data.get('full_name', '').strip()
        phone_number = data.get('phone_number', '').strip()
        address = data.get('address', '').strip()
        email = data.get('email', '').strip() if data.get('email') else None

        if not full_name:
            errors.append("Customer full name is required.")
        elif len(full_name) > 120:
            errors.append("Full name cannot exceed 120 characters.")

        if not phone_number:
            errors.append("Phone number is required.")
        elif not CustomerValidator.validate_phone_format(phone_number):
            errors.append("Please enter a valid phone number (at least 7 digits).")
        elif CustomerRepository.get_by_phone(phone_number):
            errors.append("A customer with this phone number already exists.")

        if not address:
            errors.append("Customer address is required.")

        if email and not CustomerValidator.validate_email_format(email):
            errors.append("Please enter a valid email address.")

        return errors

    @staticmethod
    def validate_customer_update(customer_id, data):
        """Validate payload for updating an existing customer."""
        errors = []
        existing_customer = CustomerRepository.get_by_id(customer_id)
        if not existing_customer:
            return ["Customer not found."]

        full_name = data.get('full_name', '').strip()
        phone_number = data.get('phone_number', '').strip()
        address = data.get('address', '').strip()
        email = data.get('email', '').strip() if data.get('email') else None

        if not full_name:
            errors.append("Customer full name is required.")
        elif len(full_name) > 120:
            errors.append("Full name cannot exceed 120 characters.")

        if not phone_number:
            errors.append("Phone number is required.")
        elif not CustomerValidator.validate_phone_format(phone_number):
            errors.append("Please enter a valid phone number.")
        else:
            cust_by_phone = CustomerRepository.get_by_phone(phone_number)
            if cust_by_phone and cust_by_phone.id != customer_id:
                errors.append("A customer with this phone number already exists.")

        if not address:
            errors.append("Customer address is required.")

        if email and not CustomerValidator.validate_email_format(email):
            errors.append("Please enter a valid email address.")

        return errors
