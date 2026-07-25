"""
OrderRepository for database access operations on Order and OrderItem models.
"""

from datetime import datetime
from app.extensions import db
from app.models.order import Order
from app.models.order_item import OrderItem
from app.models.customer import Customer


class OrderRepository:
    """Repository class encapsulating Order database queries."""

    @staticmethod
    def get_by_id(order_id, include_deleted=False):
        """Retrieve order by primary key ID."""
        query = Order.query.filter_by(id=order_id)
        if not include_deleted:
            query = query.filter_by(is_deleted=False)
        return query.first()

    @staticmethod
    def get_by_number(order_number, include_deleted=False):
        """Retrieve order by order reference number (e.g. KF-2026-00001)."""
        if not order_number:
            return None
        query = Order.query.filter(db.func.lower(Order.order_number) == order_number.strip().lower())
        if not include_deleted:
            query = query.filter_by(is_deleted=False)
        return query.first()

    @staticmethod
    def generate_order_number():
        """
        Generates the next sequential order number (e.g., KF-2026-00001).
        """
        current_year = datetime.utcnow().year
        year_prefix = f"KF-{current_year}-"

        # Find latest order created in current year
        last_order = Order.query.filter(Order.order_number.like(f"{year_prefix}%")).order_by(Order.id.desc()).first()

        if not last_order:
            return f"{year_prefix}00001"

        try:
            last_seq = int(last_order.order_number.split('-')[-1])
            next_seq = last_seq + 1
        except (ValueError, IndexError):
            next_seq = last_order.id + 1

        return f"{year_prefix}{next_seq:05d}"

    @staticmethod
    def filter_orders(search_query=None, status=None, payment_status=None, customer_id=None, page=1, per_page=10, include_deleted=False):
        """
        Filter orders with optional search term, processing status, payment status, customer, and pagination.

        Returns:
            Pagination object
        """
        query = Order.query

        if not include_deleted:
            query = query.filter_by(is_deleted=False)

        if customer_id:
            query = query.filter_by(customer_id=customer_id)

        if status and status.strip() and status.strip().lower() != 'all':
            query = query.filter(db.func.lower(Order.order_status) == status.strip().lower())

        if payment_status and payment_status.strip() and payment_status.strip().lower() != 'all':
            query = query.filter(db.func.lower(Order.payment_status) == payment_status.strip().lower())

        if search_query and search_query.strip():
            search_pattern = f"%{search_query.strip()}%"
            query = query.join(Customer).filter(
                db.or_(
                    Order.order_number.ilike(search_pattern),
                    Customer.full_name.ilike(search_pattern),
                    Customer.customer_code.ilike(search_pattern),
                    Customer.phone_number.ilike(search_pattern)
                )
            )

        return query.order_by(Order.created_at.desc()).paginate(
            page=page, per_page=per_page, error_out=False
        )

    @staticmethod
    def create(order, items):
        """
        Add and commit order record along with line items.
        """
        db.session.add(order)
        db.session.flush()  # assign order.id

        for item in items:
            item.order_id = order.id
            item.calculate_subtotal()
            db.session.add(item)

        db.session.flush()
        order.recalculate_totals()
        db.session.commit()
        return order

    @staticmethod
    def update_status(order, new_status):
        """Update processing status of an order."""
        order.order_status = new_status
        db.session.commit()
        return order

    @staticmethod
    def cancel(order):
        """Cancels an order per BR-ORD-004."""
        order.order_status = 'Cancelled'
        db.session.commit()
        return order

    @staticmethod
    def soft_delete(order):
        """Performs soft delete on order record."""
        order.is_deleted = True
        db.session.commit()
        return order
