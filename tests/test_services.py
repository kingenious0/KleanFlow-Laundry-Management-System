"""
Unit & Integration Test Suite for Phase 4 Laundry Services Module.
"""

import pytest
from app import create_app
from app.extensions import db
from app.models.user import User
from app.models.service import Service
from app.services_layer.service_service import ServiceService


@pytest.fixture
def app():
    """Create test application instance with SQLite in-memory database."""
    app = create_app('testing')
    app.config.update({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
        'WTF_CSRF_ENABLED': False
    })

    with app.app_context():
        db.create_all()
        # Seed default test users
        admin = User(
            full_name="Admin User",
            email="admin@test.com",
            phone_number="0240000001",
            role="Administrator",
            status="Active"
        )
        admin.set_password("Admin123!")

        manager = User(
            full_name="Manager User",
            email="manager@test.com",
            phone_number="0240000002",
            role="Manager",
            status="Active"
        )
        manager.set_password("Manager123!")

        cashier = User(
            full_name="Cashier User",
            email="cashier@test.com",
            phone_number="0240000003",
            role="Cashier",
            status="Active"
        )
        cashier.set_password("Cashier123!")

        db.session.add_all([admin, manager, cashier])
        db.session.commit()

        yield app

        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    """Test client instance."""
    return app.test_client()


def login_client(client, email, password):
    """Helper function to log in a user."""
    return client.post('/auth/login', data={
        'email': email,
        'password': password
    }, follow_redirects=True)


def test_create_service_success(app):
    """Test successful service creation (BR-SER-001)."""
    with app.app_context():
        data = {
            'service_name': 'Premium Wash & Fold',
            'category': 'Wash & Fold',
            'price': '25.50',
            'description': 'Comprehensive wash, dry, and professional fold service.',
            'status': 'Active'
        }
        service, errors = ServiceService.create_service(data)
        assert len(errors) == 0
        assert service is not None
        assert service.id is not None
        assert service.service_name == 'Premium Wash & Fold'
        assert service.category == 'Wash & Fold'
        assert float(service.price) == 25.50
        assert service.status == 'Active'
        assert service.is_deleted is False


def test_create_service_duplicate_name(app):
    """Test creating a service with a duplicate name fails (BR-SER-001)."""
    with app.app_context():
        data = {
            'service_name': 'Express Ironing',
            'category': 'Ironing & Pressing',
            'price': '15.00',
            'status': 'Active'
        }
        s1, e1 = ServiceService.create_service(data)
        assert len(e1) == 0

        # Attempt to create second service with same name
        s2, e2 = ServiceService.create_service(data)
        assert s2 is None
        assert len(e2) > 0
        assert "already exists" in e2[0]


def test_create_service_negative_price(app):
    """Test creating a service with negative price fails."""
    with app.app_context():
        data = {
            'service_name': 'Invalid Price Service',
            'category': 'General',
            'price': '-10.00',
            'status': 'Active'
        }
        service, errors = ServiceService.create_service(data)
        assert service is None
        assert len(errors) > 0
        assert "cannot be negative" in errors[0]


def test_update_service_success(app):
    """Test updating service name, category, and price (BR-SER-003)."""
    with app.app_context():
        s, _ = ServiceService.create_service({
            'service_name': 'Basic Wash',
            'category': 'Wash & Fold',
            'price': '10.00',
            'status': 'Active'
        })

        updated, errors = ServiceService.update_service(s.id, {
            'service_name': 'Super Basic Wash',
            'category': 'Wash & Fold',
            'price': '12.00',
            'status': 'Active'
        })
        assert len(errors) == 0
        assert updated.service_name == 'Super Basic Wash'
        assert float(updated.price) == 12.00


def test_toggle_service_status(app):
    """Test toggling service status from Active to Inactive and back (BR-SER-002)."""
    with app.app_context():
        s, _ = ServiceService.create_service({
            'service_name': 'Dry Clean Suit',
            'category': 'Dry Cleaning',
            'price': '45.00',
            'status': 'Active'
        })
        assert s.status == 'Active'

        toggled, msg = ServiceService.toggle_service_status(s.id)
        assert toggled.status == 'Inactive'
        assert "status updated to 'Inactive'" in msg

        toggled_back, msg_back = ServiceService.toggle_service_status(s.id)
        assert toggled_back.status == 'Active'
        assert "status updated to 'Active'" in msg_back


def test_soft_delete_service(app):
    """Test soft deleting a service removes it from active queries."""
    with app.app_context():
        s, _ = ServiceService.create_service({
            'service_name': 'Obsolete Dye Service',
            'category': 'Specialty & Repairs',
            'price': '50.00',
            'status': 'Active'
        })

        success, msg = ServiceService.soft_delete_service(s.id)
        assert success is True

        # Ensure service is marked deleted
        deleted_svc = ServiceService.get_service_by_id(s.id, include_deleted=True)
        assert deleted_svc.is_deleted is True
        assert deleted_svc.status == 'Inactive'

        # Ensure standard lookup returns None
        assert ServiceService.get_service_by_id(s.id, include_deleted=False) is None


def test_services_web_routes_rbac(client, app):
    """Test role-based access control on HTTP service endpoints."""
    with app.app_context():
        # Create sample service
        s, _ = ServiceService.create_service({
            'service_name': 'Standard Ironing',
            'category': 'Ironing & Pressing',
            'price': '8.00',
            'status': 'Active'
        })
        service_id = s.id

    # 1. Unauthenticated request -> redirects to login
    res = client.get('/services/')
    assert res.status_code == 302
    assert '/auth/login' in res.location

    # 2. Cashier login -> can view index and active API, but blocked from create/edit/delete
    login_client(client, 'cashier@test.com', 'Cashier123!')

    res = client.get('/services/')
    assert res.status_code == 200
    assert b'Standard Ironing' in res.data
    assert b'GH&#34; 8.00' in res.data or b'8.00' in res.data

    res_api = client.get('/services/api/active')
    assert res_api.status_code == 200
    json_data = res_api.get_json()
    assert json_data['success'] is True
    assert len(json_data['data']) == 1
    assert json_data['data'][0]['service_name'] == 'Standard Ironing'

    # Cashier denied from create (redirected with 302 to dashboard)
    res_create = client.get('/services/create', follow_redirects=True)
    assert res_create.status_code == 200
    assert b'You do not have permission' in res_create.data

    client.get('/auth/logout')

    # 3. Administrator login -> full access to create/edit/toggle/delete
    login_client(client, 'admin@test.com', 'Admin123!')

    res_create_page = client.get('/services/create')
    assert res_create_page.status_code == 200

    res_post_create = client.post('/services/create', data={
        'service_name': 'Curtains Cleaning',
        'category': 'Specialty & Repairs',
        'price': '60.00',
        'description': 'Heavy curtain wash and steam.',
        'status': 'Active'
    }, follow_redirects=True)
    assert res_post_create.status_code == 200
    assert b'Curtains Cleaning' in res_post_create.data

    # Toggle status
    res_toggle = client.post(f'/services/{service_id}/toggle-status', follow_redirects=True)
    assert res_toggle.status_code == 200

    # Soft delete
    res_delete = client.post(f'/services/{service_id}/delete', follow_redirects=True)
    assert res_delete.status_code == 200
    assert b'removed successfully' in res_delete.data
