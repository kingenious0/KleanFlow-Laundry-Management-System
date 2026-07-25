"""
PickupRepository for database operations on Pickup model.
"""

from app.extensions import db
from app.models.pickup import Pickup
from app.models.order import Order
from app.models.customer import Customer


class PickupRepository:
    """Repository class for Pickup database queries."""

    @staticmethod
    def get_by_id(pickup_id):
        return db.session.get(Pickup, pickup_id)

    @staticmethod
    def get_by_order_id(order_id):
        return Pickup.query.filter_by(order_id=order_id).first()

    @staticmethod
    def filter_pickups(status=None, assigned_staff_id=None, page=1, per_page=10):
        query = Pickup.query.join(Order).join(Customer)

        if status and status.strip() and status.strip().lower() != 'all':
            query = query.filter(db.func.lower(Pickup.status) == status.strip().lower())

        if assigned_staff_id:
            query = query.filter_by(assigned_staff=assigned_staff_id)

        return query.order_by(Pickup.created_at.desc()).paginate(page=page, per_page=per_page, error_out=False)

    @staticmethod
    def create(pickup):
        db.session.add(pickup)
        db.session.commit()
        return pickup

    @staticmethod
    def update(pickup):
        db.session.commit()
        return pickup
