"""
Payment input validation module for KleanFlow payment processing.
"""

from app.repositories.order_repository import OrderRepository


class PaymentValidator:
    """Validator class for payment recording operations."""

    VALID_PAYMENT_METHODS = ['Cash', 'Mobile Money', 'Card', 'Bank Transfer']

    @staticmethod
    def validate_payment_recording(data):
        """
        Validate payload for recording a payment (BR-PAY-001 & BR-PAY-002).
        """
        errors = []
        order_id_raw = data.get('order_id')
        amount_raw = data.get('amount')
        payment_method = data.get('payment_method', 'Cash').strip() if data.get('payment_method') else 'Cash'

        if not order_id_raw:
            errors.append("Order selection is required (BR-PAY-001).")
            return errors

        try:
            order_id = int(order_id_raw)
            order = OrderRepository.get_by_id(order_id)
            if not order:
                errors.append("Selected order does not exist or has been removed.")
                return errors
            elif order.order_status == 'Cancelled':
                errors.append("Payments cannot be recorded on cancelled orders (BR-ORD-004).")
                return errors
            elif float(order.balance) <= 0:
                errors.append("This order is already fully paid (Balance: GH₵ 0.00).")
                return errors
        except (ValueError, TypeError):
            errors.append("Invalid order ID format.")
            return errors

        if amount_raw is None or str(amount_raw).strip() == '':
            errors.append("Payment amount is required.")
        else:
            try:
                amount_val = float(amount_raw)
                if amount_val <= 0:
                    errors.append("Payment amount must be greater than zero (BR-PAY-002).")
                elif amount_val > float(order.balance) + 0.001:  # Allow minimal float rounding
                    errors.append(f"Payment amount (GH₵ {amount_val:.2f}) cannot exceed remaining balance (GH₵ {float(order.balance):.2f}) (BR-PAY-002).")
            except (ValueError, TypeError):
                errors.append("Payment amount must be a valid number.")

        if payment_method not in PaymentValidator.VALID_PAYMENT_METHODS:
            errors.append(f"Payment method must be one of: {', '.join(PaymentValidator.VALID_PAYMENT_METHODS)}.")

        return errors
