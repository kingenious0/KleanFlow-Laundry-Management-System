"""
PaymentRepository for database access operations on Payment model.
"""

from datetime import datetime
from app.extensions import db
from app.models.payment import Payment
from app.models.order import Order
from app.models.customer import Customer


class PaymentRepository:
    """Repository class encapsulating Payment database queries."""

    @staticmethod
    def get_by_id(payment_id):
        """Retrieve payment by primary key ID."""
        return Payment.query.filter_by(id=payment_id).first()

    @staticmethod
    def get_by_reference(payment_reference):
        """Retrieve payment by reference string (e.g. PAY-2026-00001)."""
        if not payment_reference:
            return None
        return Payment.query.filter(db.func.lower(Payment.payment_reference) == payment_reference.strip().lower()).first()

    @staticmethod
    def generate_payment_reference():
        """Generates sequential payment reference (e.g. PAY-2026-00001)."""
        current_year = datetime.utcnow().year
        year_prefix = f"PAY-{current_year}-"

        last_payment = Payment.query.filter(Payment.payment_reference.like(f"{year_prefix}%")).order_by(Payment.id.desc()).first()

        if not last_payment:
            return f"{year_prefix}00001"

        try:
            last_seq = int(last_payment.payment_reference.split('-')[-1])
            next_seq = last_seq + 1
        except (ValueError, IndexError):
            next_seq = last_payment.id + 1

        return f"{year_prefix}{next_seq:05d}"

    @staticmethod
    def filter_payments(search_query=None, payment_method=None, order_id=None, page=1, per_page=10):
        """Filter payments with optional search query, payment method, order ID, and pagination."""
        query = Payment.query

        if order_id:
            query = query.filter_by(order_id=order_id)

        if payment_method and payment_method.strip() and payment_method.strip().lower() != 'all':
            query = query.filter(db.func.lower(Payment.payment_method) == payment_method.strip().lower())

        if search_query and search_query.strip():
            search_pattern = f"%{search_query.strip()}%"
            query = query.join(Order).join(Customer).filter(
                db.or_(
                    Payment.payment_reference.ilike(search_pattern),
                    Order.order_number.ilike(search_pattern),
                    Customer.full_name.ilike(search_pattern),
                    Customer.phone_number.ilike(search_pattern)
                )
            )

        return query.order_by(Payment.payment_date.desc()).paginate(
            page=page, per_page=per_page, error_out=False
        )

    @staticmethod
    def create(payment):
        """Add and commit new payment record."""
        db.session.add(payment)
        db.session.commit()
        return payment
