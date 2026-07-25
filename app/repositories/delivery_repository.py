"""
DeliveryRepository for database operations on Delivery model.
"""

from app.extensions import db
from app.models.delivery import Delivery
from app.models.order import Order
from app.models.customer import Customer


class DeliveryRepository:
    """Repository class for Delivery database queries."""

    @staticmethod
    def get_by_id(delivery_id):
        return db.session.get(Delivery, delivery_id)

    @staticmethod
    def get_by_order_id(order_id):
        return Delivery.query.filter_by(order_id=order_id).first()

    @staticmethod
    def filter_deliveries(status=None, assigned_staff_id=None, page=1, per_page=10):
        query = Delivery.query.join(Order).join(Customer)

        if status and status.strip() and status.strip().lower() != 'all':
            query = query.filter(db.func.lower(Delivery.delivery_status) == status.strip().lower())

        if assigned_staff_id:
            query = query.filter_by(assigned_staff=assigned_staff_id)

        return query.order_by(Delivery.created_at.desc()).paginate(page=page, per_page=per_page, error_out=False)

    @staticmethod
    def create(delivery):
        db.session.add(delivery)
        db.session.commit()
        return delivery

    @staticmethod
    def update(delivery):
        db.session.commit()
        return delivery
