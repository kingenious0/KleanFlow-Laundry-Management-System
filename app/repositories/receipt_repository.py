"""
ReceiptRepository for database access operations on Receipt model.
"""

from datetime import datetime
from app.extensions import db
from app.models.receipt import Receipt
from app.models.order import Order
from app.models.customer import Customer


class ReceiptRepository:
    """Repository class encapsulating Receipt database queries."""

    @staticmethod
    def get_by_id(receipt_id):
        """Retrieve receipt by primary key ID."""
        return Receipt.query.filter_by(id=receipt_id).first()

    @staticmethod
    def get_by_number(receipt_number):
        """Retrieve receipt by receipt reference number (e.g. REC-2026-00001)."""
        if not receipt_number:
            return None
        return Receipt.query.filter(db.func.lower(Receipt.receipt_number) == receipt_number.strip().lower()).first()

    @staticmethod
    def get_by_payment_id(payment_id):
        """Retrieve receipt by associated payment ID."""
        return Receipt.query.filter_by(payment_id=payment_id).first()

    @staticmethod
    def generate_receipt_number():
        """Generates sequential receipt number (e.g. REC-2026-00001)."""
        current_year = datetime.utcnow().year
        year_prefix = f"REC-{current_year}-"

        last_receipt = Receipt.query.filter(Receipt.receipt_number.like(f"{year_prefix}%")).order_by(Receipt.id.desc()).first()

        if not last_receipt:
            return f"{year_prefix}00001"

        try:
            last_seq = int(last_receipt.receipt_number.split('-')[-1])
            next_seq = last_seq + 1
        except (ValueError, IndexError):
            next_seq = last_receipt.id + 1

        return f"{year_prefix}{next_seq:05d}"

    @staticmethod
    def filter_receipts(search_query=None, page=1, per_page=10):
        """Filter receipts with optional search term and pagination."""
        query = Receipt.query

        if search_query and search_query.strip():
            search_pattern = f"%{search_query.strip()}%"
            query = query.join(Order).join(Customer).filter(
                db.or_(
                    Receipt.receipt_number.ilike(search_pattern),
                    Order.order_number.ilike(search_pattern),
                    Customer.full_name.ilike(search_pattern),
                    Customer.phone_number.ilike(search_pattern)
                )
            )

        return query.order_by(Receipt.printed_at.desc()).paginate(
            page=page, per_page=per_page, error_out=False
        )

    @staticmethod
    def create(receipt):
        """Add and commit new receipt record."""
        db.session.add(receipt)
        db.session.commit()
        return receipt
