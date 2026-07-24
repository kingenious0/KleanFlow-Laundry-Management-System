"""
AuthService handling user authentication and session management.
"""

from flask_login import login_user, logout_user
from app.repositories.user_repository import UserRepository
from app.validators.user_validator import UserValidator


class AuthService:
    """Service layer class for authentication operations."""

    @staticmethod
    def authenticate_user(email, password):
        """
        Authenticates user credentials.

        Returns:
            tuple: (User object or None, error_message or None)
        """
        validation_errors = UserValidator.validate_login_input(email, password)
        if validation_errors:
            return None, validation_errors[0]

        user = UserRepository.get_by_email(email)

        if not user:
            return None, "Invalid email address or password."

        if user.status != 'Active':
            return None, "Your account has been deactivated. Please contact an administrator."

        if not user.check_password(password):
            return None, "Invalid email address or password."

        return user, None

    @staticmethod
    def login_session(user, remember=False):
        """Logs user into session using Flask-Login."""
        if not user or user.status != 'Active':
            return False
        return login_user(user, remember=remember)

    @staticmethod
    def logout_session():
        """Logs user out of current session."""
        logout_user()
        return True
