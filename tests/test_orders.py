"""
Unit & Integration Test Suite for Phase 5 Order Management Module.
"""

import json
import pytest
from app import create_app
from app.extensions import db
from app.models.user import User
from app.models.customer import Customer
from app.models.service import Service
from app.services_layer.order_service import OrderService
from app.services_layer.customer_service import CustomerService
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

        cashier = User(
            full_name="Cashier User",
            email="cashier@test.com",
            phone_number="0240000003",
            role="Cashier",
            status="Active"
        )
        cashier.set_password("Cashier123!")

        db.session.add_all([admin, cashier])
        db.session.commit()

        # Seed default test customer
        cust, _ = CustomerService.create_customer({
            'full_name': 'Kofi Mensah',
            'phone_number': '0244112233',
            'address': 'Accra Digital Center, Ring Road'
        })

        # Seed active & inactive test services
        s1, _ = ServiceService.create_service({
            'service_name': 'Wash & Fold (per kg)',
            'category': 'Wash & Fold',
            'price': '15.00',
            'status': 'Active'
        })

        s2, _ = ServiceService.create_service({
            'service_name': 'Dry Clean Suit',
            'category': 'Dry Cleaning',
            'price': '40.00',
            'status': 'Active'
        })

        s3_inactive, _ = ServiceService.create_service({
            'service_name': 'Retired Dyeing Service',
            'category': 'Specialty',
            'price': '60.00',
            'status': 'Inactive'
        })

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


def test_create_order_success(app):
    """Test successful order creation with items & total calculation (BR-ORD-001 & BR-ORD-002)."""
    with app.app_context():
        cust = Customer.query.first()
        services = Service.query.filter_by(status='Active').all()

        data = {
            'customer_id': cust.id,
            'items': [
                {'service_id': services[0].id, 'quantity': 2, 'clothing_type': 'Casual shirts'},
                {'service_id': services[1].id, 'quantity': 1, 'clothing_type': 'Black 2-piece suit'}
            ]
        }

        order, errors = OrderService.create_order(data)
        assert len(errors) == 0
        assert order is not None
        assert order.order_number.startswith('KF-')
        assert order.customer_id == cust.id
        assert len(order.items) == 2
        # Math check: (2 * 15.00) + (1 * 40.00) = 70.00
        assert float(order.total_amount) == 70.00
        assert float(order.balance) == 70.00
        assert order.order_status == 'Pending'
        assert order.payment_status == 'Unpaid'


def test_create_order_inactive_service_rejected(app):
    """Test creating an order with an inactive service is rejected (BR-SER-002)."""
    with app.app_context():
        cust = Customer.query.first()
        inactive_svc = Service.query.filter_by(status='Inactive').first()

        data = {
            'customer_id': cust.id,
            'items': [
                {'service_id': inactive_svc.id, 'quantity': 1, 'clothing_type': 'Old coat'}
            ]
        }

        order, errors = OrderService.create_order(data)
        assert order is None
        assert len(errors) > 0
        assert "inactive and cannot be selected" in errors[0]


def test_order_status_workflow_transitions(app):
    """Test processing order status lifecycle transitions (BR-ORD-003)."""
    with app.app_context():
        cust = Customer.query.first()
        svc = Service.query.filter_by(status='Active').first()

        order, _ = OrderService.create_order({
            'customer_id': cust.id,
            'items': [{'service_id': svc.id, 'quantity': 1}]
        })
        assert order.order_status == 'Pending'

        # Advance to Washing
        OrderService.update_order_status(order.id, 'Washing')
        assert order.order_status == 'Washing'

        # Advance to Ironing
        OrderService.update_order_status(order.id, 'Ironing')
        assert order.order_status == 'Ironing'

        # Advance to Ready
        OrderService.update_order_status(order.id, 'Ready')
        assert order.order_status == 'Ready'

        # Advance to Completed
        OrderService.update_order_status(order.id, 'Completed')
        assert order.order_status == 'Completed'


def test_order_cancellation(app):
    """Test order cancellation rules (BR-ORD-004)."""
    with app.app_context():
        cust = Customer.query.first()
        svc = Service.query.filter_by(status='Active').first()

        order, _ = OrderService.create_order({
            'customer_id': cust.id,
            'items': [{'service_id': svc.id, 'quantity': 1}]
        })

        # Cancel order while in Pending
        success, msg = OrderService.cancel_order(order.id)
        assert success is True
        assert order.order_status == 'Cancelled'

        # Attempt to change status of cancelled order fails
        _, errors = OrderService.update_order_status(order.id, 'Washing')
        assert len(errors) > 0
        assert "Cannot change status of a cancelled order" in errors[0]


def test_orders_web_routes(client, app):
    """Test HTTP endpoints for Order Management."""
    with app.app_context():
        cust = Customer.query.first()
        svc = Service.query.filter_by(status='Active').first()

    # Log in as Cashier
    login_client(client, 'cashier@test.com', 'Cashier123!')

    # 1. View Orders index
    res_index = client.get('/orders/')
    assert res_index.status_code == 200

    # 2. View Create Order page
    res_create_page = client.get('/orders/create')
    assert res_create_page.status_code == 200

    # 3. Post new order
    items_json = json.dumps([{'service_id': svc.id, 'quantity': 2, 'clothing_type': 'White shirts'}])
    res_post_order = client.post('/orders/create', data={
        'customer_id': cust.id,
        'items_json': items_json
    }, follow_redirects=True)

    assert res_post_order.status_code == 200
    assert b'created successfully' in res_post_order.data
    assert b'White shirts' in res_post_order.data

    # Find created order id
    with app.app_context():
        created_order = OrderService.list_orders().items[0]
        order_id = created_order.id

    # 4. View Order details
    res_show = client.get(f'/orders/{order_id}')
    assert res_show.status_code == 200
    assert created_order.order_number.encode() in res_show.data

    # 5. Update Status via HTTP POST
    res_status = client.post(f'/orders/{order_id}/status', data={
        'order_status': 'Washing'
    }, follow_redirects=True)
    assert res_status.status_code == 200
    assert b'Washing' in res_status.data

    # 6. Cancel order via HTTP POST
    res_cancel = client.post(f'/orders/{order_id}/cancel', follow_redirects=True)
    assert res_cancel.status_code == 200
    assert b'has been cancelled' in res_cancel.data
