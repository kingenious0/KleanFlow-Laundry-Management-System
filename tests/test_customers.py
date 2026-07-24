"""
Test suite for Customer Management module (Phase 3).
"""

import pytest
from app import create_app
from app.extensions import db
from app.models.user import User
from app.models.customer import Customer


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
            full_name="Admin Test",
            email="admin@kleanflow.com",
            phone_number="0200000000",
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
            full_name="Staff Test",
            email="staff@kleanflow.com",
            phone_number="0201111111",
            role="Laundry Staff",
            status="Active"
        )
        staff.set_password("Staff123!")
        db.session.add(staff)
        db.session.commit()
        return staff.id


def login_client(client, email, password):
    return client.post('/auth/login', data={'email': email, 'password': password}, follow_redirects=True)


def test_customer_list_authenticated(client, admin_user):
    """Authenticated user can view customer list page."""
    login_client(client, 'admin@kleanflow.com', 'Admin123!')
    response = client.get('/customers/')
    assert response.status_code == 200
    assert b"Customer Directory" in response.data


def test_create_customer_success(client, admin_user):
    """Registers a new customer with auto-generated code and valid inputs."""
    login_client(client, 'admin@kleanflow.com', 'Admin123!')
    response = client.post('/customers/create', data={
        'full_name': 'Kwame Mensah',
        'phone_number': '0245555555',
        'email': 'kwame@example.com',
        'address': 'House 12, East Legon, Accra'
    }, follow_redirects=True)

    assert response.status_code == 200
    assert b"registered successfully" in response.data.lower()

    with client.application.app_context():
        cust = Customer.query.filter_by(phone_number='0245555555').first()
        assert cust is not None
        assert cust.full_name == 'Kwame Mensah'
        assert cust.customer_code.startswith('CUST-')
        assert cust.is_deleted is False


def test_create_customer_missing_required_fields(client, admin_user):
    """Validation fails if required address or phone is missing."""
    login_client(client, 'admin@kleanflow.com', 'Admin123!')
    response = client.post('/customers/create', data={
        'full_name': 'No Address Cust',
        'phone_number': '0246666666',
        'address': ''
    }, follow_redirects=True)

    assert response.status_code == 200
    assert b"address is required" in response.data.lower()


def test_create_customer_duplicate_phone(client, admin_user):
    """Validation fails if phone number already belongs to another active customer (BR-CUS-002)."""
    login_client(client, 'admin@kleanflow.com', 'Admin123!')

    # First customer
    client.post('/customers/create', data={
        'full_name': 'Cust One',
        'phone_number': '0247777777',
        'address': 'Accra Central'
    })

    # Duplicate phone attempt
    response = client.post('/customers/create', data={
        'full_name': 'Cust Two',
        'phone_number': '0247777777',
        'address': 'Tema Station'
    }, follow_redirects=True)

    assert response.status_code == 200
    assert b"already exists" in response.data.lower()


def test_customer_search_and_pagination(client, admin_user):
    """Tests customer search filter and pagination."""
    login_client(client, 'admin@kleanflow.com', 'Admin123!')

    with client.application.app_context():
        for i in range(1, 15):
            c = Customer(
                customer_code=f"CUST-{i:04d}",
                full_name=f"Customer Test {i}",
                phone_number=f"02400000{i:02d}",
                address=f"Location {i}"
            )
            db.session.add(c)
        db.session.commit()

    # Search filter test
    search_resp = client.get('/customers/?search=Test 12')
    assert search_resp.status_code == 200
    assert b"Customer Test 12" in search_resp.data
    assert b"Customer Test 14" not in search_resp.data

    # Pagination test (page 1)
    page1_resp = client.get('/customers/?page=1')
    assert page1_resp.status_code == 200
    assert b"Customer Test 14" in page1_resp.data


def test_customer_profile_rendering(client, admin_user):
    """Tests viewing customer profile page."""
    login_client(client, 'admin@kleanflow.com', 'Admin123!')

    with client.application.app_context():
        cust = Customer(
            customer_code="CUST-9999",
            full_name="Profile Test Customer",
            phone_number="0248888888",
            address="Airport Residential Area"
        )
        db.session.add(cust)
        db.session.commit()
        cust_id = cust.id

    response = client.get(f'/customers/{cust_id}')
    assert response.status_code == 200
    assert b"Profile Test Customer" in response.data
    assert b"CUST-9999" in response.data


def test_edit_customer(client, admin_user):
    """Tests editing customer details."""
    login_client(client, 'admin@kleanflow.com', 'Admin123!')

    with client.application.app_context():
        cust = Customer(
            customer_code="CUST-8888",
            full_name="Old Name",
            phone_number="0249999999",
            address="Old Address"
        )
        db.session.add(cust)
        db.session.commit()
        cust_id = cust.id

    response = client.post(f'/customers/{cust_id}/edit', data={
        'full_name': 'New Updated Name',
        'phone_number': '0249999999',
        'email': 'newemail@example.com',
        'address': 'New Updated Address'
    }, follow_redirects=True)

    assert response.status_code == 200
    assert b"updated successfully" in response.data.lower()

    with client.application.app_context():
        updated_c = db.session.get(Customer, cust_id)
        assert updated_c.full_name == 'New Updated Name'
        assert updated_c.address == 'New Updated Address'


def test_soft_delete_customer_admin(client, admin_user):
    """Administrator can soft delete customer record."""
    login_client(client, 'admin@kleanflow.com', 'Admin123!')

    with client.application.app_context():
        cust = Customer(
            customer_code="CUST-7777",
            full_name="To Be Deleted",
            phone_number="0241234567",
            address="Spintex"
        )
        db.session.add(cust)
        db.session.commit()
        cust_id = cust.id

    response = client.post(f'/customers/{cust_id}/delete', follow_redirects=True)
    assert response.status_code == 200
    assert b"successfully removed" in response.data.lower()

    with client.application.app_context():
        deleted_c = db.session.get(Customer, cust_id)
        assert deleted_c is not None
        assert deleted_c.is_deleted is True


def test_soft_delete_customer_staff_denied(client, staff_user):
    """Laundry Staff cannot soft delete customer record."""
    login_client(client, 'staff@kleanflow.com', 'Staff123!')

    with client.application.app_context():
        cust = Customer(
            customer_code="CUST-6666",
            full_name="Protected Customer",
            phone_number="0247654321",
            address="Osu"
        )
        db.session.add(cust)
        db.session.commit()
        cust_id = cust.id

    response = client.post(f'/customers/{cust_id}/delete', follow_redirects=True)
    assert response.status_code == 200
    assert b"do not have permission" in response.data.lower()

    with client.application.app_context():
        protected_c = db.session.get(Customer, cust_id)
        assert protected_c.is_deleted is False


def test_customer_json_api_search(client, admin_user):
    """Tests customer auto-complete JSON API."""
    login_client(client, 'admin@kleanflow.com', 'Admin123!')

    with client.application.app_context():
        c = Customer(
            customer_code="CUST-5555",
            full_name="API Search Target",
            phone_number="0205555555",
            address="Cantonments"
        )
        db.session.add(c)
        db.session.commit()

    response = client.get('/customers/api/search?q=Target')
    assert response.status_code == 200
    data = response.get_json()
    assert data['success'] is True
    assert len(data['data']) > 0
    assert data['data'][0]['full_name'] == "API Search Target"
