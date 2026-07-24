"""
Phase 1 Foundation & Authentication Verification Test Suite.
"""

import pytest
from app import create_app
from app.extensions import db, login_manager
from app.models import User, Customer, Service


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


def test_app_created(app):
    assert app is not None
    assert app.testing is True
    assert login_manager is not None


def test_dashboard_route_requires_auth(client):
    response = client.get('/', follow_redirects=False)
    assert response.status_code == 302
    assert '/auth/login' in response.headers['Location']


def test_dashboard_route_authenticated(client, app):
    with app.app_context():
        admin = User(full_name="Admin Test", email="admin@kleanflow.com", role="Administrator", status="Active")
        admin.set_password("Admin123!")
        db.session.add(admin)
        db.session.commit()

    client.post('/auth/login', data={'email': 'admin@kleanflow.com', 'password': 'Admin123!'})
    response = client.get('/')
    assert response.status_code == 200
    assert b"Klean" in response.data
    assert b"Dashboard Overview" in response.data


def test_login_route(client):
    response = client.get('/auth/login')
    assert response.status_code == 200
    assert b"Sign In" in response.data


def test_404_page(client):
    response = client.get('/nonexistent-page-route')
    assert response.status_code == 404
    assert b"404" in response.data


def test_models_creation(app):
    with app.app_context():
        user = User(full_name="Admin Test", email="admin@kleanflow.com", role="Administrator")
        user.set_password("password123!")
        db.session.add(user)

        customer = Customer(customer_code="CUST-001", full_name="John Doe", phone_number="1234567890")
        db.session.add(customer)

        service = Service(service_name="Wash & Fold", price=15.50)
        db.session.add(service)

        db.session.commit()

        assert User.query.count() == 1
        assert Customer.query.count() == 1
        assert Service.query.count() == 1

        fetched_user = User.query.first()
        assert fetched_user.check_password("password123!") is True
