"""
ServiceRepository for database access operations on Service model.
"""

from app.extensions import db
from app.models.service import Service


class ServiceRepository:
    """Repository class encapsulating Service database queries."""

    @staticmethod
    def get_by_id(service_id, include_deleted=False):
        """Retrieve service by primary key ID."""
        query = Service.query.filter_by(id=service_id)
        if not include_deleted:
            query = query.filter_by(is_deleted=False)
        return query.first()

    @staticmethod
    def get_by_name(service_name, include_deleted=False):
        """Retrieve service by name (case-insensitive)."""
        if not service_name:
            return None
        query = Service.query.filter(db.func.lower(Service.service_name) == service_name.strip().lower())
        if not include_deleted:
            query = query.filter_by(is_deleted=False)
        return query.first()

    @staticmethod
    def filter_services(search_query=None, category=None, status=None, page=1, per_page=12, include_deleted=False):
        """
        Filter services with optional search term, category, status, and pagination.

        Returns:
            Pagination object
        """
        query = Service.query

        if not include_deleted:
            query = query.filter_by(is_deleted=False)

        if category and category.strip() and category.strip().lower() != 'all':
            query = query.filter(db.func.lower(Service.category) == category.strip().lower())

        if status and status.strip() and status.strip().lower() != 'all':
            query = query.filter(db.func.lower(Service.status) == status.strip().lower())

        if search_query and search_query.strip():
            search_pattern = f"%{search_query.strip()}%"
            query = query.filter(
                db.or_(
                    Service.service_name.ilike(search_pattern),
                    Service.category.ilike(search_pattern),
                    Service.description.ilike(search_pattern)
                )
            )

        return query.order_by(Service.category.asc(), Service.service_name.asc()).paginate(
            page=page, per_page=per_page, error_out=False
        )

    @staticmethod
    def get_active_services():
        """Retrieve all active, non-deleted services for order creation."""
        return Service.query.filter_by(is_deleted=False, status='Active').order_by(
            Service.category.asc(), Service.service_name.asc()
        ).all()

    @staticmethod
    def get_categories():
        """Retrieve unique categories from non-deleted services."""
        categories = db.session.query(Service.category).filter_by(is_deleted=False).distinct().all()
        return [cat[0] for cat in categories if cat[0]]

    @staticmethod
    def create(service):
        """Add and commit new service record."""
        db.session.add(service)
        db.session.commit()
        return service

    @staticmethod
    def update(service):
        """Commit updates to an existing service record."""
        db.session.commit()
        return service

    @staticmethod
    def toggle_status(service):
        """Toggles status between Active and Inactive."""
        service.status = 'Inactive' if service.status == 'Active' else 'Active'
        db.session.commit()
        return service

    @staticmethod
    def soft_delete(service):
        """Performs soft delete on service record."""
        service.is_deleted = True
        service.status = 'Inactive'
        db.session.commit()
        return service
