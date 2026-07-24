"""
UserService handling business logic and security constraints for User Management CRUD.
"""

from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.validators.user_validator import UserValidator


class UserService:
    """Service layer class for user administration."""

    @staticmethod
    def get_user_by_id(user_id):
        """Retrieve user by ID."""
        return UserRepository.get_by_id(user_id)

    @staticmethod
    def list_users(search_query=None, role=None, status=None, page=1, per_page=10):
        """Retrieve paginated user list with optional filtering."""
        return UserRepository.filter_users(
            search_query=search_query,
            role=role,
            status=status,
            page=page,
            per_page=per_page
        )

    @staticmethod
    def create_user(data):
        """
        Creates a new user after validation.

        Returns:
            tuple: (created User or None, list of error messages)
        """
        errors = UserValidator.validate_user_creation(data)
        if errors:
            return None, errors

        user = User(
            full_name=data.get('full_name', '').strip(),
            email=data.get('email', '').strip().lower(),
            phone_number=data.get('phone_number', '').strip() if data.get('phone_number') else None,
            role=data.get('role', 'Laundry Staff').strip(),
            status=data.get('status', 'Active').strip()
        )
        user.set_password(data.get('password', ''))

        created_user = UserRepository.create(user)
        return created_user, []

    @staticmethod
    def update_user(user_id, data, current_user_id=None):
        """
        Updates an existing user record.

        Returns:
            tuple: (updated User or None, list of error messages)
        """
        user = UserRepository.get_by_id(user_id)
        if not user:
            return None, ["User not found."]

        errors = UserValidator.validate_user_update(user_id, data)
        if errors:
            return None, errors

        new_role = data.get('role', user.role).strip()
        new_status = data.get('status', user.status).strip()

        # Enforce last administrator protection
        if user.role == 'Administrator' and (new_role != 'Administrator' or new_status != 'Active'):
            active_admins = UserRepository.count_admins()
            if active_admins <= 1:
                return None, ["Cannot demote or deactivate the system's only active Administrator."]

        user.full_name = data.get('full_name', user.full_name).strip()
        user.email = data.get('email', user.email).strip().lower()
        user.phone_number = data.get('phone_number', '').strip() if data.get('phone_number') else None
        user.role = new_role
        user.status = new_status

        new_password = data.get('password', '')
        if new_password:
            user.set_password(new_password)

        updated_user = UserRepository.update(user)
        return updated_user, []

    @staticmethod
    def toggle_user_status(user_id, current_user_id):
        """
        Toggles active/inactive status of a user.

        Returns:
            tuple: (success boolean, message string)
        """
        if user_id == current_user_id:
            return False, "You cannot deactivate your own logged-in account."

        user = UserRepository.get_by_id(user_id)
        if not user:
            return False, "User not found."

        if user.status == 'Active':
            if user.role == 'Administrator' and UserRepository.count_admins() <= 1:
                return False, "Cannot deactivate the system's only active Administrator."
            user.status = 'Inactive'
        else:
            user.status = 'Active'

        UserRepository.update(user)
        return True, f"User status updated to {user.status}."

    @staticmethod
    def delete_user(user_id, current_user_id):
        """
        Deletes a user account.

        Returns:
            tuple: (success boolean, message string)
        """
        if user_id == current_user_id:
            return False, "You cannot delete your own logged-in account."

        user = UserRepository.get_by_id(user_id)
        if not user:
            return False, "User not found."

        if user.role == 'Administrator' and UserRepository.count_admins() <= 1:
            return False, "Cannot delete the system's only active Administrator."

        UserRepository.delete(user)
        return True, "User successfully deleted."

    @staticmethod
    def change_password(user_id, current_password, new_password):
        """
        Changes user's own password after verifying current password.

        Returns:
            tuple: (success boolean, error message or None)
        """
        user = UserRepository.get_by_id(user_id)
        if not user:
            return False, "User not found."

        if not user.check_password(current_password):
            return False, "Current password is incorrect."

        errors = UserValidator.validate_password_strength(new_password)
        if errors:
            return False, errors[0]

        user.set_password(new_password)
        UserRepository.update(user)
        return True, None
