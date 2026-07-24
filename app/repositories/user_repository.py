"""
UserRepository for database access operations on User model.
"""

from app.extensions import db
from app.models.user import User


class UserRepository:
    """Repository class encapsulating User database queries."""

    @staticmethod
    def get_by_id(user_id):
        """Retrieve user by primary key ID."""
        return db.session.get(User, user_id)

    @staticmethod
    def get_by_email(email):
        """Retrieve user by email address (case-insensitive)."""
        if not email:
            return None
        return User.query.filter(db.func.lower(User.email) == email.strip().lower()).first()

    @staticmethod
    def get_by_phone(phone_number):
        """Retrieve user by phone number."""
        if not phone_number:
            return None
        return User.query.filter_by(phone_number=phone_number.strip()).first()

    @staticmethod
    def get_all():
        """Retrieve all users ordered by creation date descending."""
        return User.query.order_by(User.created_at.desc()).all()

    @staticmethod
    def filter_users(search_query=None, role=None, status=None, page=1, per_page=10):
        """
        Filter users with optional search term, role, status, and pagination.

        Returns:
            Pagination object
        """
        query = User.query

        if search_query:
            search_pattern = f"%{search_query.strip()}%"
            query = query.filter(
                db.or_(
                    User.full_name.ilike(search_pattern),
                    User.email.ilike(search_pattern),
                    User.phone_number.ilike(search_pattern)
                )
            )

        if role:
            query = query.filter_by(role=role)

        if status:
            query = query.filter_by(status=status)

        return query.order_by(User.created_at.desc()).paginate(
            page=page, per_page=per_page, error_out=False
        )

    @staticmethod
    def count_admins():
        """Count active administrator accounts."""
        return User.query.filter_by(role='Administrator', status='Active').count()

    @staticmethod
    def create(user):
        """Add and commit new user record."""
        db.session.add(user)
        db.session.commit()
        return user

    @staticmethod
    def update(user):
        """Commit updates to an existing user record."""
        db.session.commit()
        return user

    @staticmethod
    def delete(user):
        """Delete user record."""
        db.session.delete(user)
        db.session.commit()
        return True
