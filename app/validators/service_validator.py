"""
Service input validation module for KleanFlow laundry services.
"""

from app.repositories.service_repository import ServiceRepository


class ServiceValidator:
    """Validator class for laundry service operations."""

    VALID_STATUSES = ['Active', 'Inactive']
    VALID_CATEGORIES = ['Wash & Fold', 'Dry Cleaning', 'Ironing & Pressing', 'Specialty & Repairs', 'Pickup & Delivery', 'General']

    @staticmethod
    def validate_service_creation(data):
        """
        Validate payload for creating a new laundry service (BR-SER-001).
        """
        errors = []
        service_name = data.get('service_name', '').strip() if data.get('service_name') else ''
        category = data.get('category', '').strip() if data.get('category') else 'General'
        description = data.get('description', '').strip() if data.get('description') else ''
        price_raw = data.get('price')
        status = data.get('status', 'Active').strip() if data.get('status') else 'Active'

        if not service_name:
            errors.append("Service name is required.")
        elif len(service_name) < 2 or len(service_name) > 120:
            errors.append("Service name must be between 2 and 120 characters.")
        elif ServiceRepository.get_by_name(service_name):
            errors.append(f"A service named '{service_name}' already exists.")

        if not category:
            errors.append("Category is required.")
        elif len(category) > 50:
            errors.append("Category name cannot exceed 50 characters.")

        if price_raw is None or str(price_raw).strip() == '':
            errors.append("Price is required.")
        else:
            try:
                price_val = float(price_raw)
                if price_val < 0:
                    errors.append("Price cannot be negative.")
                elif price_val > 999999.99:
                    errors.append("Price exceeds maximum allowed value.")
            except (ValueError, TypeError):
                errors.append("Price must be a valid number.")

        if status not in ServiceValidator.VALID_STATUSES:
            errors.append(f"Status must be one of: {', '.join(ServiceValidator.VALID_STATUSES)}.")

        return errors

    @staticmethod
    def validate_service_update(service_id, data):
        """
        Validate payload for updating an existing laundry service.
        """
        errors = []
        existing_service = ServiceRepository.get_by_id(service_id)
        if not existing_service:
            return ["Service not found."]

        service_name = data.get('service_name', '').strip() if data.get('service_name') else ''
        category = data.get('category', '').strip() if data.get('category') else 'General'
        price_raw = data.get('price')
        status = data.get('status', existing_service.status).strip() if data.get('status') else existing_service.status

        if not service_name:
            errors.append("Service name is required.")
        elif len(service_name) < 2 or len(service_name) > 120:
            errors.append("Service name must be between 2 and 120 characters.")
        else:
            svc_by_name = ServiceRepository.get_by_name(service_name)
            if svc_by_name and svc_by_name.id != service_id:
                errors.append(f"A service named '{service_name}' already exists.")

        if not category:
            errors.append("Category is required.")
        elif len(category) > 50:
            errors.append("Category name cannot exceed 50 characters.")

        if price_raw is None or str(price_raw).strip() == '':
            errors.append("Price is required.")
        else:
            try:
                price_val = float(price_raw)
                if price_val < 0:
                    errors.append("Price cannot be negative.")
                elif price_val > 999999.99:
                    errors.append("Price exceeds maximum allowed value.")
            except (ValueError, TypeError):
                errors.append("Price must be a valid number.")

        if status not in ServiceValidator.VALID_STATUSES:
            errors.append(f"Status must be one of: {', '.join(ServiceValidator.VALID_STATUSES)}.")

        return errors
