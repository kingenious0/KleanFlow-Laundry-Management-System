"""
Database Seeder for KleanFlow Laundry Management System.
Populates default Manager and Laundry Attendant user accounts.
"""

from app import create_app
from app.extensions import db
from app.models.user import User

app = create_app()

def seed_database():
    with app.app_context():
        print("Seeding KleanFlow database...")
        db.create_all()

        # Manager
        manager = User.query.filter_by(email='manager@kleanflow.com').first()
        if not manager:
            manager = User(
                full_name='Sarah Manager',
                email='manager@kleanflow.com',
                phone_number='0201111111',
                role='Manager',
                status='Active'
            )
            manager.set_password('manager123')
            db.session.add(manager)

        # Laundry Attendant
        attendant = User.query.filter_by(email='attendant@kleanflow.com').first()
        if not attendant:
            attendant = User(
                full_name='Kofi Attendant',
                email='attendant@kleanflow.com',
                phone_number='0202222222',
                role='Laundry Attendant',
                status='Active'
            )
            attendant.set_password('attendant123')
            db.session.add(attendant)

        db.session.commit()
        print("  [+] Created Default Accounts (Manager, Laundry Attendant)")
        print("\n=== KleanFlow Seeding Completed Successfully ===")
        print("Credentials:")
        print("  Manager          : manager@kleanflow.com   / manager123")
        print("  Laundry Attendant: attendant@kleanflow.com / attendant123")

if __name__ == '__main__':
    seed_database()
