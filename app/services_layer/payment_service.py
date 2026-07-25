"""
PaymentService handling business logic for Payment Recording and Balance Tracking.
"""

from app.models.payment import Payment
from app.models.receipt import Receipt
from app.repositories.payment_repository import PaymentRepository
from app.repositories.receipt_repository import ReceiptRepository
from app.repositories.order_repository import OrderRepository
from app.validators.payment_validator import PaymentValidator


class PaymentService:
    """Service layer class for payments and financial transactions."""

    @staticmethod
    def get_payment_by_id(payment_id):
        """Retrieve payment by ID."""
        return PaymentRepository.get_by_id(payment_id)

    @staticmethod
    def list_payments(search_query=None, payment_method=None, order_id=None, page=1, per_page=10):
        """Retrieve paginated payments list with optional filters."""
        return PaymentRepository.filter_payments(
            search_query=search_query,
            payment_method=payment_method,
            order_id=order_id,
            page=page,
            per_page=per_page
        )

    @staticmethod
    def record_payment(data, received_by_user_id=None):
        """
        Records a payment for an order, updates balance & payment status, and auto-generates a receipt (BR-PAY-001..003 & BR-REC-001).

        Returns:
            tuple: (created Payment or None, created Receipt or None, list of error messages)
        """
        errors = PaymentValidator.validate_payment_recording(data)
        if errors:
            return None, None, errors

        order_id = int(data['order_id'])
        amount = float(data['amount'])
        payment_method = data.get('payment_method', 'Cash').strip() or 'Cash'
        payment_reference = PaymentRepository.generate_payment_reference()

        payment = Payment(
            order_id=order_id,
            payment_reference=payment_reference,
            payment_method=payment_method,
            amount=amount,
            payment_status='Completed',
            received_by=received_by_user_id
        )

        created_payment = PaymentRepository.create(payment)

        # Update order balance & payment status per BR-PAY-003
        order = OrderRepository.get_by_id(order_id)
        order.paid_amount = float(order.paid_amount) + amount
        order.update_payment_status()
        OrderRepository.update_status(order, order.order_status)

        # Auto-generate official Receipt per BR-REC-001
        receipt_number = ReceiptRepository.generate_receipt_number()
        receipt = Receipt(
            receipt_number=receipt_number,
            order_id=order.id,
            payment_id=created_payment.id
        )
        created_receipt = ReceiptRepository.create(receipt)

        return created_payment, created_receipt, []
