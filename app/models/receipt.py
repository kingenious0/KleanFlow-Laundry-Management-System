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

    def __repr__(self):
        return f"<Receipt id={self.id} receipt_number='{self.receipt_number}'>"
