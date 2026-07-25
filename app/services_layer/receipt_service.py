"""
ReceiptService handling business logic for Official Receipt generation and printing.
"""

from app.models.receipt import Receipt
from app.repositories.receipt_repository import ReceiptRepository


class ReceiptService:
    """Service layer class for official receipts administration."""

    @staticmethod
    def get_receipt_by_id(receipt_id):
        """Retrieve receipt by ID."""
        return ReceiptRepository.get_by_id(receipt_id)

    @staticmethod
    def get_receipt_by_number(receipt_number):
        """Retrieve receipt by reference number."""
        return ReceiptRepository.get_by_number(receipt_number)

    @staticmethod
    def list_receipts(search_query=None, page=1, per_page=10):
        """Retrieve paginated receipts list."""
        return ReceiptRepository.filter_receipts(
            search_query=search_query,
            page=page,
            per_page=per_page
        )

    @staticmethod
    def get_receipt_printable_data(receipt_id):
        """
        Formats complete receipt dataset for thermal/A4 printable views per BR-REC-002.

        Returns:
            dict: receipt, order, customer, items, payment breakdown, and business info
        """
        receipt = ReceiptRepository.get_by_id(receipt_id)
        if not receipt:
            return None

        order = receipt.order
        customer = order.customer if order else None
        payment = receipt.payment

        return {
            'id': receipt.id,
            'receipt': receipt,
            'receipt_number': receipt.receipt_number,
            'printed_at': receipt.printed_at,
            'issued_at': receipt.printed_at,
            'order': order,
            'order_number': order.order_number if order else 'N/A',
            'customer': customer,
            'items': order.items if order else [],
            'payment': payment,
            'payment_reference': payment.payment_reference if payment else 'N/A',
            'payment_method': payment.payment_method if payment else 'Cash',
            'amount_paid': float(payment.amount) if payment else 0.0,
            'total_order_amount': float(order.total_amount) if order else 0.0,
            'total_paid_so_far': float(order.paid_amount) if order else 0.0,
            'remaining_balance': float(order.balance) if order else 0.0,
            'business_name': 'KleanFlow Laundry',
            'business_address': 'Asafo By-Pass, Kumasi, Ghana',
            'business_phone': '+233 55 375 1016',
            'business_email': 'support@kleanflow.com',
            'business': {
                'name': 'KleanFlow Laundry',
                'tagline': 'Premium Laundry, Dry Cleaning & Delivery',
                'address': 'Asafo By-Pass, Kumasi, Ghana',
                'phone': '+233 55 375 1016',
                'email': 'support@kleanflow.com'
            }
        }
