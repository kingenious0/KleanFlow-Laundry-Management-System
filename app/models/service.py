"""
Service model for laundry services and pricing.
"""

from datetime import datetime
from app.extensions import db


class Service(db.Model):
    __tablename__ = 'services'

    id = db.Column(db.BigInteger().with_variant(db.Integer, 'sqlite'), primary_key=True, autoincrement=True)
    service_name = db.Column(db.String(120), nullable=False)
    category = db.Column(db.String(50), nullable=False, default='General')
    description = db.Column(db.Text, nullable=True)
    price = db.Column(db.Numeric(10, 2), nullable=False, default=0.00)
    status = db.Column(db.String(20), nullable=False, default='Active')
    is_deleted = db.Column(db.Boolean, default=False, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    order_items = db.relationship('OrderItem', backref='service', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'service_name': self.service_name,
            'category': self.category,
            'description': self.description,
            'price': float(self.price) if self.price is not None else 0.0,
            'status': self.status,
            'is_deleted': self.is_deleted,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

    def __repr__(self):
        return f"<Service id={self.id} name='{self.service_name}' price={self.price}>"

