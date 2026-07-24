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

    def __repr__(self):
        return f"<OrderItem id={self.id} order_id={self.order_id} service_id={self.service_id} qty={self.quantity}>"
