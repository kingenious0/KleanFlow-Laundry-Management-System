"""
Setting model for application settings and business preferences.
"""

from app.extensions import db


class Setting(db.Model):
    __tablename__ = 'settings'

    id = db.Column(db.BigInteger().with_variant(db.Integer, 'sqlite'), primary_key=True, autoincrement=True)
    business_name = db.Column(db.String(150), nullable=True, default='KleanFlow Laundry Services')
    business_phone = db.Column(db.String(20), nullable=True)
    business_email = db.Column(db.String(120), nullable=True)
    receipt_prefix = db.Column(db.String(20), nullable=True, default='RCP-')
    currency = db.Column(db.String(10), nullable=True, default='GHS')
    tax_rate = db.Column(db.Numeric(5, 2), nullable=True, default=0.00)

    def __repr__(self):
        return f"<Setting id={self.id} business='{self.business_name}'>"
