"""
Test suite for Authentication & Session Management.
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
def create_admin_user(app):
    user = User(
        full_name="Admin Test",
        email="admin@kleanflow.com",
        phone_number="0200000000",
        role="Administrator",
        status="Active"
    )
    user.set_password("Admin123!")
    with app.app_context():
        db.session.add(user)
        db.session.commit()
        return user.id


@pytest.fixture
def create_inactive_user(app):
    user = User(
        full_name="Inactive User",
        email="inactive@kleanflow.com",
        role="Cashier",
        status="Inactive"
    )
    user.set_password("Password123!")
    with app.app_context():
        db.session.add(user)
        db.session.commit()
        return user.id


def test_unauthenticated_redirect(client):
    """Test accessing protected dashboard redirects to login."""
    response = client.get('/', follow_redirects=False)
    assert response.status_code == 302
    assert '/auth/login' in response.headers['Location']


def test_login_page_renders(client):
    """Test login page renders successfully."""
    response = client.get('/auth/login')
    assert response.status_code == 200
    assert b"Sign In" in response.data


def test_successful_login(client, create_admin_user):
    """Test login with valid administrator credentials."""
    response = client.post('/auth/login', data={
        'email': 'admin@kleanflow.com',
        'password': 'Admin123!'
    }, follow_redirects=True)

    assert response.status_code == 200
    assert b"Welcome back, Admin Test!" in response.data
    assert b"Dashboard Overview" in response.data


def test_login_invalid_password(client, create_admin_user):
    """Test login fails with incorrect password."""
    response = client.post('/auth/login', data={
        'email': 'admin@kleanflow.com',
        'password': 'WrongPassword123!'
    }, follow_redirects=True)

    assert response.status_code == 200
    assert b"Invalid email address or password." in response.data


def test_login_nonexistent_email(client):
    """Test login fails with non-existent email."""
    response = client.post('/auth/login', data={
        'email': 'nobody@kleanflow.com',
        'password': 'Password123!'
    }, follow_redirects=True)

    assert response.status_code == 200
    assert b"Invalid email address or password." in response.data


def test_login_inactive_user(client, create_inactive_user):
    """Test login fails for inactive user accounts."""
    response = client.post('/auth/login', data={
        'email': 'inactive@kleanflow.com',
        'password': 'Password123!'
    }, follow_redirects=True)

    assert response.status_code == 200
    assert b"deactivated" in response.data.lower()


def test_logout(client, create_admin_user):
    """Test logout ends active session."""
    # Login first
    client.post('/auth/login', data={
        'email': 'admin@kleanflow.com',
        'password': 'Admin123!'
    })

    # Logout
    response = client.get('/auth/logout', follow_redirects=True)
    assert response.status_code == 200
    assert b"successfully logged out" in response.data.lower()

    # Verify protected page requires login again
    dash_resp = client.get('/', follow_redirects=False)
    assert dash_resp.status_code == 302
