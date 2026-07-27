"""
Database Seeder for KleanFlow Laundry Management System.
Populates default Manager and Laundry Attendant user accounts.
"""

import os
import pymysql
from urllib.parse import urlparse
from dotenv import load_dotenv

load_dotenv()

def auto_create_database():
    db_uri = os.getenv('DATABASE_URL') or os.getenv('SQLALCHEMY_DATABASE_URI', '')
    if not db_uri or 'mysql' not in db_uri:
        return
    try:
        clean_url = db_uri.replace('mysql+pymysql://', 'http://').replace('mysql://', 'http://')
        parsed = urlparse(clean_url)
        db_name = parsed.path.lstrip('/')
        host = parsed.hostname or 'localhost'
        port = parsed.port or 3306
        user = parsed.username or 'root'
        password = parsed.password or ''
        
        if db_name:
            conn = pymysql.connect(host=host, port=port, user=user, password=password)
            cursor = conn.cursor()
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS `{db_name}` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;")
            conn.commit()
            conn.close()
            print(f"[+] Ensured MySQL database `{db_name}` exists on {host}:{port}.")
    except Exception as e:
        print(f"[!] Database auto-creation notice: {e}")

auto_create_database()

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
