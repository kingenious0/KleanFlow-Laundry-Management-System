"""
Delivery model representing delivery dispatch records.
"""

from datetime import datetime
from app.extensions import db


class Delivery(db.Model):
    __tablename__ = 'deliveries'

    id = db.Column(db.BigInteger().with_variant(db.Integer, 'sqlite'), primary_key=True, autoincrement=True)
    order_id = db.Column(db.BigInteger().with_variant(db.Integer, 'sqlite'), db.ForeignKey('orders.id'), nullable=False)
    assigned_staff = db.Column(db.BigInteger().with_variant(db.Integer, 'sqlite'), db.ForeignKey('users.id'), nullable=True)
    delivery_date = db.Column(db.Date, nullable=True)
    delivery_time = db.Column(db.Time, nullable=True)
    delivery_status = db.Column(db.String(30), nullable=False, default='Waiting')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Delivery id={self.id} order_id={self.order_id} status='{self.delivery_status}'>"
