"""
OrderService handling business logic for Order Management.
"""

from app.models.order import Order
from app.models.order_item import OrderItem
from app.repositories.order_repository import OrderRepository
from app.repositories.service_repository import ServiceRepository
from app.repositories.customer_repository import CustomerRepository
from app.validators.order_validator import OrderValidator


class OrderService:
    """Service layer class for order administration."""

    @staticmethod
    def get_order_by_id(order_id, include_deleted=False):
        """Retrieve order by ID."""
        return OrderRepository.get_by_id(order_id, include_deleted=include_deleted)

    @staticmethod
    def get_order_by_number(order_number):
        """Retrieve order by reference number."""
        return OrderRepository.get_by_number(order_number)

    @staticmethod
    def list_orders(search_query=None, status=None, payment_status=None, customer_id=None, page=1, per_page=10):
        """Retrieve paginated orders list with filters."""
        return OrderRepository.filter_orders(
            search_query=search_query,
            status=status,
            payment_status=payment_status,
            customer_id=customer_id,
            page=page,
            per_page=per_page
        )

    @staticmethod
    def create_order(data, created_by_user_id=None):
        """
        Creates a new laundry order along with order line items.

        Returns:
            tuple: (created Order or None, list of error messages)
        """
        errors = OrderValidator.validate_order_creation(data)
        if errors:
            return None, errors

        customer_id = int(data['customer_id'])
        order_number = OrderRepository.generate_order_number()

        order = Order(
            order_number=order_number,
            customer_id=customer_id,
            total_amount=0.00,
            paid_amount=0.00,
            balance=0.00,
            payment_status='Unpaid',
            order_status='Pending',
            created_by=created_by_user_id,
            is_deleted=False
        )

        items_objects = []
        for item_data in data.get('items', []):
            service_id = int(item_data['service_id'])
            service = ServiceRepository.get_by_id(service_id)
            quantity = int(item_data.get('quantity', 1))
            clothing_type = item_data.get('clothing_type', '').strip() if item_data.get('clothing_type') else None
            unit_price = float(service.price) if service else 0.00

            item = OrderItem(
                service_id=service_id,
                clothing_type=clothing_type,
                quantity=quantity,
                unit_price=unit_price,
                subtotal=quantity * unit_price
            )
            items_objects.append(item)

        created_order = OrderRepository.create(order, items_objects)
        return created_order, []

    @staticmethod
    def update_order_status(order_id, new_status):
        """
        Updates processing status of an order (BR-ORD-003).

        Returns:
            tuple: (updated Order or None, message or error list)
        """
        errors = OrderValidator.validate_status_update(order_id, new_status)
        if errors:
            return None, errors

        order = OrderRepository.get_by_id(order_id)
        OrderRepository.update_status(order, new_status)
        return order, [f"Order '{order.order_number}' status updated to '{new_status}'."]

    @staticmethod
    def cancel_order(order_id):
        """
        Cancels an order per BR-ORD-004.

        Returns:
            tuple: (success boolean, message string)
        """
        order = OrderRepository.get_by_id(order_id)
        if not order:
            return False, "Order not found."

        if not order.can_be_cancelled():
            return False, f"Order '{order.order_number}' cannot be cancelled as it is currently '{order.order_status}'."

        OrderRepository.cancel(order)
        return True, f"Order '{order.order_number}' has been cancelled."
