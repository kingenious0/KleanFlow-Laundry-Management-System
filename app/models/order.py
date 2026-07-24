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

    def __repr__(self):
        return f"<Order id={self.id} number='{self.order_number}' status='{self.order_status}'>"
