"""
Pickup model representing laundry pickup request records.
"""

from datetime import datetime
from app.extensions import db


class Pickup(db.Model):
    __tablename__ = 'pickups'

    id = db.Column(db.BigInteger().with_variant(db.Integer, 'sqlite'), primary_key=True, autoincrement=True)
    order_id = db.Column(db.BigInteger().with_variant(db.Integer, 'sqlite'), db.ForeignKey('orders.id'), nullable=False)
    assigned_staff = db.Column(db.BigInteger().with_variant(db.Integer, 'sqlite'), db.ForeignKey('users.id'), nullable=True)
    pickup_date = db.Column(db.Date, nullable=True)
    pickup_time = db.Column(db.Time, nullable=True)
    status = db.Column(db.String(30), nullable=False, default='Pending')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Pickup id={self.id} order_id={self.order_id} status='{self.status}'>"
