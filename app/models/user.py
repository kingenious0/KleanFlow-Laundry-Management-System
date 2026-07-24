"""
User model representing employee accounts in KleanFlow.
"""

from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app.extensions import db


class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.BigInteger().with_variant(db.Integer, 'sqlite'), primary_key=True, autoincrement=True)
    full_name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    phone_number = db.Column(db.String(20), unique=True, nullable=True, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(50), nullable=False, default='Laundry Staff')
    status = db.Column(db.String(20), nullable=False, default='Active')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    orders_created = db.relationship('Order', foreign_keys='Order.created_by', backref='creator', lazy=True)
    payments_received = db.relationship('Payment', foreign_keys='Payment.received_by', backref='receiver', lazy=True)
    pickups_assigned = db.relationship('Pickup', foreign_keys='Pickup.assigned_staff', backref='staff', lazy=True)
    deliveries_assigned = db.relationship('Delivery', foreign_keys='Delivery.assigned_staff', backref='staff', lazy=True)
    notifications = db.relationship('Notification', backref='user', lazy=True)

    def set_password(self, password):
        """Hashes and sets user password."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Verifies password against stored hash."""
        return check_password_hash(self.password_hash, password)

    def is_active_user(self):
        """Returns True if user status is Active."""
        return self.status == 'Active'

    def has_role(self, *roles):
        """Returns True if user role is within specified roles."""
        return self.role in roles

    def is_admin(self):
        return self.role == 'Administrator'

    def is_manager(self):
        return self.role in ['Administrator', 'Manager']

    def __repr__(self):
        return f"<User id={self.id} email='{self.email}' role='{self.role}'>"

