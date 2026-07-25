"""
Order model for laundry order records.
"""

from datetime import datetime
from app.extensions import db


class Order(db.Model):
    __tablename__ = 'orders'

    id = db.Column(db.BigInteger().with_variant(db.Integer, 'sqlite'), primary_key=True, autoincrement=True)
    order_number = db.Column(db.String(50), unique=True, nullable=False, index=True)
    customer_id = db.Column(db.BigInteger().with_variant(db.Integer, 'sqlite'), db.ForeignKey('customers.id'), nullable=False)
    total_amount = db.Column(db.Numeric(10, 2), nullable=False, default=0.00)
    paid_amount = db.Column(db.Numeric(10, 2), nullable=False, default=0.00)
    balance = db.Column(db.Numeric(10, 2), nullable=False, default=0.00)
    payment_status = db.Column(db.String(30), nullable=False, default='Pending', index=True)
    order_status = db.Column(db.String(30), nullable=False, default='Pending', index=True)
    created_by = db.Column(db.BigInteger().with_variant(db.Integer, 'sqlite'), db.ForeignKey('users.id'), nullable=True)
    is_deleted = db.Column(db.Boolean, default=False, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    items = db.relationship('OrderItem', backref='order', lazy=True, cascade='all, delete-orphan')
    payments = db.relationship('Payment', backref='order', lazy=True)
    receipts = db.relationship('Receipt', backref='order', lazy=True)
    pickup = db.relationship('Pickup', backref='order', uselist=False, lazy=True)
    delivery = db.relationship('Delivery', backref='order', uselist=False, lazy=True)

    def can_be_cancelled(self):
        """Order can be cancelled if not Completed and not already Cancelled."""
        return self.order_status not in ['Completed', 'Cancelled']

    def update_payment_status(self):
        """Updates payment status based on paid_amount and total_amount."""
        tot = float(self.total_amount) if self.total_amount is not None else 0.0
        paid = float(self.paid_amount) if self.paid_amount is not None else 0.0
        self.balance = max(0.0, tot - paid)

        if paid <= 0:
            self.payment_status = 'Unpaid'
        elif paid < tot:
            self.payment_status = 'Partially Paid'
        else:
            self.payment_status = 'Paid'

    def recalculate_totals(self):
        """Recalculates total_amount and balance based on order line items."""
        total = sum([float(item.subtotal) for item in self.items if item.subtotal is not None])
        self.total_amount = total
        self.update_payment_status()

    def to_dict(self):
        return {
            'id': self.id,
            'order_number': self.order_number,
            'customer_id': self.customer_id,
            'customer_name': self.customer.full_name if self.customer else None,
            'total_amount': float(self.total_amount) if self.total_amount is not None else 0.0,
            'paid_amount': float(self.paid_amount) if self.paid_amount is not None else 0.0,
            'balance': float(self.balance) if self.balance is not None else 0.0,
            'payment_status': self.payment_status,
            'order_status': self.order_status,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'items_count': len(self.items) if self.items else 0
        }

    def __repr__(self):
        return f"<Order id={self.id} number='{self.order_number}' status='{self.order_status}'>"

