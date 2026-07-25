"""
OrderItem model representing individual line items in a laundry order.
"""

from app.extensions import db


class OrderItem(db.Model):
    __tablename__ = 'order_items'

    id = db.Column(db.BigInteger().with_variant(db.Integer, 'sqlite'), primary_key=True, autoincrement=True)
    order_id = db.Column(db.BigInteger().with_variant(db.Integer, 'sqlite'), db.ForeignKey('orders.id'), nullable=False)
    service_id = db.Column(db.BigInteger().with_variant(db.Integer, 'sqlite'), db.ForeignKey('services.id'), nullable=False)
    clothing_type = db.Column(db.String(100), nullable=True)
    quantity = db.Column(db.Integer, nullable=False, default=1)
    unit_price = db.Column(db.Numeric(10, 2), nullable=False, default=0.00)
    subtotal = db.Column(db.Numeric(10, 2), nullable=False, default=0.00)

    def calculate_subtotal(self):
        """Calculates subtotal = quantity * unit_price."""
        qty = int(self.quantity) if self.quantity else 0
        price = float(self.unit_price) if self.unit_price is not None else 0.0
        self.subtotal = qty * price
        return self.subtotal

    def to_dict(self):
        return {
            'id': self.id,
            'order_id': self.order_id,
            'service_id': self.service_id,
            'service_name': self.service.service_name if self.service else None,
            'clothing_type': self.clothing_type,
            'quantity': self.quantity,
            'unit_price': float(self.unit_price) if self.unit_price is not None else 0.0,
            'subtotal': float(self.subtotal) if self.subtotal is not None else 0.0
        }

    def __repr__(self):
        return f"<OrderItem id={self.id} order_id={self.order_id} service_id={self.service_id} qty={self.quantity}>"

