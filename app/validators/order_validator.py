"""
Order input validation module for KleanFlow order management.
"""

from app.repositories.customer_repository import CustomerRepository
from app.repositories.service_repository import ServiceRepository
from app.repositories.order_repository import OrderRepository


class OrderValidator:
    """Validator class for order creation and status workflows."""

    VALID_ORDER_STATUSES = ['Pending', 'Received', 'Washing', 'Ironing', 'Ready', 'Completed', 'Cancelled']

    @staticmethod
    def validate_order_creation(data):
        """
        Validate order creation payload (BR-ORD-001 & BR-SER-002).
        """
        errors = []
        customer_id_raw = data.get('customer_id')
        items = data.get('items', [])

        if not customer_id_raw:
            errors.append("Customer selection is required.")
        else:
            try:
                customer_id = int(customer_id_raw)
                customer = CustomerRepository.get_by_id(customer_id)
                if not customer:
                    errors.append("Selected customer does not exist or has been removed.")
            except (ValueError, TypeError):
                errors.append("Invalid customer ID format.")

        if not items or not isinstance(items, list) or len(items) == 0:
            errors.append("Order must contain at least one service item.")
        else:
            for idx, item in enumerate(items, start=1):
                service_id_raw = item.get('service_id')
                quantity_raw = item.get('quantity', 1)

                if not service_id_raw:
                    errors.append(f"Item #{idx}: Service selection is required.")
                else:
                    try:
                        service_id = int(service_id_raw)
                        service = ServiceRepository.get_by_id(service_id)
                        if not service:
                            errors.append(f"Item #{idx}: Selected service does not exist.")
                        elif service.status != 'Active':
                            errors.append(f"Item #{idx}: Service '{service.service_name}' is currently inactive and cannot be selected (BR-SER-002).")
                    except (ValueError, TypeError):
                        errors.append(f"Item #{idx}: Invalid service ID format.")

                try:
                    qty = int(quantity_raw)
                    if qty < 1:
                        errors.append(f"Item #{idx}: Quantity must be at least 1.")
                    elif qty > 10000:
                        errors.append(f"Item #{idx}: Quantity exceeds maximum limit.")
                except (ValueError, TypeError):
                    errors.append(f"Item #{idx}: Quantity must be a valid integer.")

        return errors

    @staticmethod
    def validate_status_update(order_id, new_status):
        """
        Validate status transition (BR-ORD-003 & BR-ORD-004).
        """
        errors = []
        order = OrderRepository.get_by_id(order_id)
        if not order:
            return ["Order not found."]

        if new_status not in OrderValidator.VALID_ORDER_STATUSES:
            errors.append(f"Invalid order status. Allowed: {', '.join(OrderValidator.VALID_ORDER_STATUSES)}.")

        if order.order_status == 'Cancelled':
            errors.append("Cannot change status of a cancelled order.")

        if order.order_status == 'Completed' and new_status != 'Completed':
            errors.append("Completed orders are locked and cannot revert status.")

        return errors
