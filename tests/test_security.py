import pytest
from app import create_app
from app.extensions import db
from app.models import User, Customer, Service, Order, Payment


@pytest.fixture
def app():
    app = create_app('testing')
    app.config.update({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
        'WTF_CSRF_ENABLED': False
    })
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def setup_users(app):
    admin = User(full_name="Admin User", email="admin@sec.com", phone_number="0201111111", role="Administrator", status="Active")
    admin.set_password("AdminPass123!")

    cashier = User(full_name="Cashier User", email="cashier@sec.com", phone_number="0202222222", role="Cashier", status="Active")
    cashier.set_password("CashierPass123!")

    inactive_admin = User(full_name="Inactive Admin", email="inactive@sec.com", phone_number="0203333333", role="Administrator", status="Inactive")
    inactive_admin.set_password("AdminPass123!")

    db.session.add_all([admin, cashier, inactive_admin])
    db.session.commit()
    return {"admin": admin, "cashier": cashier, "inactive_admin": inactive_admin}


def login(client, email, password):
    return client.post('/auth/login', data={'email': email, 'password': password}, follow_redirects=True)


class TestAuthenticationSecurity:
    def test_inactive_user_cannot_login(self, client, setup_users):
        """Ensures inactive account login attempt is rejected."""
        response = login(client, 'inactive@sec.com', 'AdminPass123!')
        assert b"deactivated" in response.data or b"Your account has been deactivated" in response.data

    def test_unauthenticated_protected_route_access(self, client):
        """Ensures unauthenticated requests to protected endpoints redirect to login."""
        protected_urls = ['/', '/users/', '/customers/', '/services/', '/orders/', '/payments/', '/reports/']
        for url in protected_urls:
            res = client.get(url)
            assert res.status_code == 302
            assert '/auth/login' in res.location


class TestRBACBoundaries:
    def test_cashier_restricted_endpoints(self, client, setup_users):
        """Ensures Cashier role cannot access Admin/Manager-restricted routes."""
        login(client, 'cashier@sec.com', 'CashierPass123!')

        admin_urls = [
            '/users/',
            '/users/create',
            '/services/create',
            '/reports/',
            '/reports/revenue',
            '/reports/customers'
        ]

        for url in admin_urls:
            res = client.get(url, follow_redirects=True)
            assert b"do not have permission" in res.data or res.status_code == 403


class TestSQLInjectionIsolation:
    def test_sqli_payload_in_customer_search(self, client, setup_users):
        """Verifies customer search with SQL injection payload executes safely without SQL error."""
        login(client, 'admin@sec.com', 'AdminPass123!')
        sqli_payload = "' OR '1'='1'; DROP TABLE customers; --"
        res = client.get(f'/customers/?search={sqli_payload}')
        assert res.status_code == 200
        # Verify table still exists by querying customers
        with client.application.app_context():
            assert db.session.query(Customer).count() >= 0

    def test_sqli_payload_in_order_search(self, client, setup_users):
        """Verifies order search with SQL injection payload executes safely."""
        login(client, 'admin@sec.com', 'AdminPass123!')
        sqli_payload = "ORD' UNION SELECT * FROM users --"
        res = client.get(f'/orders/?search={sqli_payload}')
        assert res.status_code == 200

    def test_sqli_payload_in_payment_search(self, client, setup_users):
        """Verifies payment search with SQL injection payload executes safely."""
        login(client, 'admin@sec.com', 'AdminPass123!')
        sqli_payload = "PAY'; SELECT pg_sleep(5); --"
        res = client.get(f'/payments/?search={sqli_payload}')
        assert res.status_code == 200


class TestXSSProtection:
    def test_xss_script_tag_in_customer_profile(self, client, setup_users):
        """Verifies stored XSS payload in customer name is safely auto-escaped in HTML template."""
        login(client, 'admin@sec.com', 'AdminPass123!')
        xss_name = "<script>alert('XSS-ATTACK')</script>"
        res = client.post('/customers/create', data={
            'full_name': xss_name,
            'phone_number': '0249999999',
            'address': 'Accra Test'
        }, follow_redirects=True)
        assert res.status_code == 200
        # Escaped HTML text should be rendered instead of raw <script> execution tag
        assert b"&lt;script&gt;alert(&#39;XSS-ATTACK&#39;)&lt;/script&gt;" in res.data or b"&lt;script&gt;" in res.data
