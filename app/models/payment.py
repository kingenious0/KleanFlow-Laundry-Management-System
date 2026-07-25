"""
Payment model representing monetary transaction records.
"""

from datetime import datetime
from app.extensions import db


class Payment(db.Model):
    __tablename__ = 'payments'

    id = db.Column(db.BigInteger().with_variant(db.Integer, 'sqlite'), primary_key=True, autoincrement=True)
    order_id = db.Column(db.BigInteger().with_variant(db.Integer, 'sqlite'), db.ForeignKey('orders.id'), nullable=False)
    payment_reference = db.Column(db.String(80), unique=True, nullable=False, index=True)
    payment_method = db.Column(db.String(30), nullable=False, default='Cash')
    amount = db.Column(db.Numeric(10, 2), nullable=False, default=0.00)
    payment_status = db.Column(db.String(30), nullable=False, default='Completed')
    received_by = db.Column(db.BigInteger().with_variant(db.Integer, 'sqlite'), db.ForeignKey('users.id'), nullable=True)
    payment_date = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    receipts = db.relationship('Receipt', backref='payment', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'order_id': self.order_id,
            'order_number': self.order.order_number if self.order else None,
            'payment_reference': self.payment_reference,
            'payment_method': self.payment_method,
            'amount': float(self.amount) if self.amount is not None else 0.0,
            'payment_status': self.payment_status,
            'received_by_id': self.received_by,
            'receiver_name': self.receiver.full_name if self.receiver else None,
            'payment_date': self.payment_date.isoformat() if self.payment_date else None
        }

    def __repr__(self):
        return f"<Payment id={self.id} ref='{self.payment_reference}' amount={self.amount}>"

