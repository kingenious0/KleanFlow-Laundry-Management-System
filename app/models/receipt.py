"""
Receipt model representing generated and printed receipt records.
"""

from datetime import datetime
from app.extensions import db


class Receipt(db.Model):
    __tablename__ = 'receipts'

    id = db.Column(db.BigInteger().with_variant(db.Integer, 'sqlite'), primary_key=True, autoincrement=True)
    receipt_number = db.Column(db.String(50), unique=True, nullable=False, index=True)
    order_id = db.Column(db.BigInteger().with_variant(db.Integer, 'sqlite'), db.ForeignKey('orders.id'), nullable=False)
    payment_id = db.Column(db.BigInteger().with_variant(db.Integer, 'sqlite'), db.ForeignKey('payments.id'), nullable=True)
    printed_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'receipt_number': self.receipt_number,
            'order_id': self.order_id,
            'order_number': self.order.order_number if self.order else None,
            'payment_id': self.payment_id,
            'payment_reference': self.payment.payment_reference if self.payment else None,
            'printed_at': self.printed_at.isoformat() if self.printed_at else None
        }

    def __repr__(self):
        return f"<Receipt id={self.id} receipt_number='{self.receipt_number}'>"

