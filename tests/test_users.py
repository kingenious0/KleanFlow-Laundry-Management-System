"""
Test suite for User Management CRUD and Role-Based Access Control (RBAC).
"""

import pytest
from app import create_app
from app.extensions import db
from app.models.user import User


@pytest.fixture
def app():
    app = create_app('testing')
    app.config['WTF_CSRF_ENABLED'] = False
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def admin_user(app):
    with app.app_context():
        admin = User(
            full_name="Admin Boss",
            email="admin@kleanflow.com",
            phone_number="0241111111",
            role="Administrator",
            status="Active"
        )
        admin.set_password("Admin123!")
        db.session.add(admin)
        db.session.commit()
        return admin.id


@pytest.fixture
def staff_user(app):
    with app.app_context():
        staff = User(
            full_name="Laundry Staff User",
            email="staff@kleanflow.com",
            phone_number="0242222222",
            role="Laundry Staff",
            status="Active"
        )
        staff.set_password("Staff123!")
        db.session.add(staff)
        db.session.commit()
        return staff.id


def login_client(client, email, password):
    return client.post('/auth/login', data={'email': email, 'password': password}, follow_redirects=True)


def test_user_management_access_admin(client, admin_user):
    """Administrator can access User Management list."""
    login_client(client, 'admin@kleanflow.com', 'Admin123!')
    response = client.get('/users/')
    assert response.status_code == 200
    assert b"Employee &amp; Staff Accounts" in response.data or b"Employee & Staff Accounts" in response.data


def test_user_management_access_staff_denied(client, staff_user):
    """Laundry Staff cannot access User Management list."""
    login_client(client, 'staff@kleanflow.com', 'Staff123!')
    response = client.get('/users/', follow_redirects=True)
    assert response.status_code == 200
    assert b"do not have permission" in response.data.lower()


def test_create_user_success(client, admin_user):
    """Administrator creates a new Cashier user successfully."""
    login_client(client, 'admin@kleanflow.com', 'Admin123!')
    response = client.post('/users/create', data={
        'full_name': 'Jane Cashier',
        'email': 'jane@kleanflow.com',
        'phone_number': '0243333333',
        'password': 'Cashier123!',
        'role': 'Cashier',
        'status': 'Active'
    }, follow_redirects=True)

    assert response.status_code == 200
    assert b"created successfully" in response.data.lower()

    with client.application.app_context():
        new_user = User.query.filter_by(email='jane@kleanflow.com').first()
        assert new_user is not None
        assert new_user.role == 'Cashier'


def test_create_user_weak_password_fails(client, admin_user):
    """Creating user with weak password fails validation."""
    login_client(client, 'admin@kleanflow.com', 'Admin123!')
    response = client.post('/users/create', data={
        'full_name': 'Weak Pwd User',
        'email': 'weak@kleanflow.com',
        'password': '123',
        'role': 'Cashier',
        'status': 'Active'
    }, follow_redirects=True)

    assert response.status_code == 200
    assert b"at least 8 characters" in response.data.lower()


def test_update_user(client, admin_user, staff_user):
    """Administrator updates staff user details."""
    login_client(client, 'admin@kleanflow.com', 'Admin123!')
    response = client.post(f'/users/{staff_user}/edit', data={
        'full_name': 'Updated Staff Name',
        'email': 'staff@kleanflow.com',
        'phone_number': '0249999999',
        'role': 'Manager',
        'status': 'Active'
    }, follow_redirects=True)

    assert response.status_code == 200
    assert b"updated successfully" in response.data.lower()

    with client.application.app_context():
        u = db.session.get(User, staff_user)
        assert u.full_name == 'Updated Staff Name'
        assert u.role == 'Manager'


def test_toggle_user_status(client, admin_user, staff_user):
    """Administrator deactivates a staff user."""
    login_client(client, 'admin@kleanflow.com', 'Admin123!')
    response = client.post(f'/users/{staff_user}/toggle-status', follow_redirects=True)
    assert response.status_code == 200
    assert b"Inactive" in response.data

    with client.application.app_context():
        u = db.session.get(User, staff_user)
        assert u.status == 'Inactive'


def test_cannot_delete_self(client, admin_user):
    """Logged in administrator cannot delete their own account."""
    login_client(client, 'admin@kleanflow.com', 'Admin123!')
    response = client.post(f'/users/{admin_user}/delete', follow_redirects=True)
    assert response.status_code == 200
    assert b"cannot delete your own" in response.data.lower()


def test_cannot_delete_last_admin(client, admin_user, staff_user):
    """System prevents deleting the last active Administrator."""
    # First create second admin
    with client.application.app_context():
        admin2 = User(full_name="Admin 2", email="admin2@kleanflow.com", role="Administrator", status="Active")
        admin2.set_password("Admin123!")
        db.session.add(admin2)
        db.session.commit()
        admin2_id = admin2.id

    # Log in as admin2 and attempt to delete original admin_user (works because admin2 is active and distinct)
    client.get('/auth/logout')
    login_client(client, 'admin2@kleanflow.com', 'Admin123!')
    del_resp = client.post(f'/users/{admin_user}/delete', follow_redirects=True)
    assert b"deleted" in del_resp.data.lower()

    # Now admin2 is the sole remaining admin. Try demoting admin2 -> blocked by last admin rule
    edit_resp = client.post(f'/users/{admin2_id}/edit', data={
        'full_name': 'Admin 2',
        'email': 'admin2@kleanflow.com',
        'role': 'Cashier',
        'status': 'Active'
    }, follow_redirects=True)
    assert b"only active administrator" in edit_resp.data.lower()

