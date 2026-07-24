"""
ServiceService handling business logic for Laundry Services management.
"""

from app.models.service import Service
from app.repositories.service_repository import ServiceRepository
from app.validators.service_validator import ServiceValidator


class ServiceService:
    """Service layer class for laundry services administration."""

    @staticmethod
    def get_service_by_id(service_id, include_deleted=False):
        """Retrieve service by ID."""
        return ServiceRepository.get_by_id(service_id, include_deleted=include_deleted)

    @staticmethod
    def list_services(search_query=None, category=None, status=None, page=1, per_page=12):
        """Retrieve paginated active services with optional filters."""
        return ServiceRepository.filter_services(
            search_query=search_query,
            category=category,
            status=status,
            page=page,
            per_page=per_page
        )

    @staticmethod
    def get_active_services():
        """Retrieve all active services for order creation."""
        return ServiceRepository.get_active_services()

    @staticmethod
    def get_categories():
        """Retrieve unique categories list."""
        return ServiceRepository.get_categories()

    @staticmethod
    def create_service(data):
        """
        Creates a new laundry service after validation.

        Returns:
            tuple: (created Service or None, list of error messages)
        """
        errors = ServiceValidator.validate_service_creation(data)
        if errors:
            return None, errors

        service = Service(
            service_name=data.get('service_name', '').strip(),
            category=data.get('category', 'General').strip() or 'General',
            description=data.get('description', '').strip() if data.get('description') else None,
            price=float(data.get('price', 0.0)),
            status=data.get('status', 'Active').strip() or 'Active',
            is_deleted=False
        )

        created_service = ServiceRepository.create(service)
        return created_service, []

    @staticmethod
    def update_service(service_id, data):
        """
        Updates an existing laundry service record.

        Returns:
            tuple: (updated Service or None, list of error messages)
        """
        service = ServiceRepository.get_by_id(service_id)
        if not service:
            return None, ["Service not found."]

        errors = ServiceValidator.validate_service_update(service_id, data)
        if errors:
            return None, errors

        service.service_name = data.get('service_name', service.service_name).strip()
        service.category = data.get('category', service.category).strip() or 'General'
        service.description = data.get('description', '').strip() if data.get('description') else None
        service.price = float(data.get('price', service.price))
        if data.get('status'):
            service.status = data.get('status').strip()

        updated_service = ServiceRepository.update(service)
        return updated_service, []

    @staticmethod
    def toggle_service_status(service_id):
        """
        Toggles service status between Active and Inactive.

        Returns:
            tuple: (toggled Service or None, message string)
        """
        service = ServiceRepository.get_by_id(service_id)
        if not service:
            return None, "Service not found."

        ServiceRepository.toggle_status(service)
        new_status = service.status
        return service, f"Service '{service.service_name}' status updated to '{new_status}'."

    @staticmethod
    def soft_delete_service(service_id):
        """
        Soft deletes a service record.

        Returns:
            tuple: (success boolean, message string)
        """
        service = ServiceRepository.get_by_id(service_id)
        if not service:
            return False, "Service not found."

        ServiceRepository.soft_delete(service)
        return True, f"Service '{service.service_name}' removed successfully."
