from datetime import datetime, date, timedelta
import pytest
from app import create_app
from app.extensions import db
from app.models import User, Customer, Service, Order, OrderItem, Payment
from app.repositories.report_repository import ReportRepository
from app.services_layer.dashboard_service import DashboardService
from app.services_layer.report_service import ReportService


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
def setup_data(app):
    # Users
    admin = User(full_name="Admin User", email="admin@test.com", phone_number="0201111111", role="Administrator", status="Active")
    admin.set_password("AdminPass123!")
    
    cashier = User(full_name="Cashier User", email="cashier@test.com", phone_number="0202222222", role="Cashier", status="Active")
    cashier.set_password("CashierPass123!")

    db.session.add_all([admin, cashier])
    db.session.commit()

    # Customer
    customer = Customer(customer_code="CUST-2026-00001", full_name="John Doe", phone_number="0241234567", email="john@example.com")
    db.session.add(customer)
    db.session.commit()

    # Service
    service1 = Service(service_name="Dry Cleaning", category="Suits", price=50.0, status="Active")
    service2 = Service(service_name="Washing", category="General", price=20.0, status="Active")
    db.session.add_all([service1, service2])
    db.session.commit()

    # Orders
    order1 = Order(
        order_number="ORD-2026-00001",
        customer_id=customer.id,
        created_by=admin.id,
        total_amount=100.0,
        paid_amount=100.0,
        balance=0.0,
        payment_status="Paid",
        order_status="Completed"
    )
    
    order2 = Order(
        order_number="ORD-2026-00002",
        customer_id=customer.id,
        created_by=admin.id,
        total_amount=60.0,
        paid_amount=20.0,
        balance=40.0,
        payment_status="Partial",
        order_status="In Progress"
    )

    db.session.add_all([order1, order2])
    db.session.commit()

    # Order Items
    item1 = OrderItem(order_id=order1.id, service_id=service1.id, unit_price=50.0, quantity=2, subtotal=100.0)
    item2 = OrderItem(order_id=order2.id, service_id=service2.id, unit_price=20.0, quantity=3, subtotal=60.0)
    db.session.add_all([item1, item2])
    db.session.commit()

    # Payments
    pay1 = Payment(
        payment_reference="PAY-2026-00001",
        order_id=order1.id,
        amount=100.0,
        payment_method="Cash",
        payment_status="Completed",
        received_by=admin.id,
        payment_date=datetime.utcnow()
    )
    pay2 = Payment(
        payment_reference="PAY-2026-00002",
        order_id=order2.id,
        amount=20.0,
        payment_method="Mobile Money",
        payment_status="Completed",
        received_by=admin.id,
        payment_date=datetime.utcnow()
    )
    db.session.add_all([pay1, pay2])
    db.session.commit()

    return {
        "admin": admin,
        "cashier": cashier,
        "customer": customer,
        "service1": service1,
        "service2": service2,
        "order1": order1,
        "order2": order2,
        "pay1": pay1,
        "pay2": pay2
    }


def test_report_repository_kpi_summary(app, setup_data):
    with app.app_context():
        kpis = ReportRepository.get_kpi_summary()
        assert kpis["today_revenue"] == 120.0
        assert kpis["monthly_revenue"] == 120.0
        assert kpis["orders_count_month"] == 2
        assert kpis["unpaid_balance"] == 40.0
        assert kpis["active_customers"] == 1


def test_report_repository_monthly_revenue_trend(app, setup_data):
    with app.app_context():
        trend = ReportRepository.get_monthly_revenue_trend(months=6)
        assert len(trend["labels"]) == 6
        assert len(trend["data"]) == 6
        assert trend["data"][-1] == 120.0


def test_report_repository_order_status_distribution(app, setup_data):
    with app.app_context():
        dist = ReportRepository.get_order_status_distribution()
        assert "Completed" in dist["labels"]
        assert "In Progress" in dist["labels"]
        assert 1 in dist["data"]


def test_report_repository_top_services(app, setup_data):
    with app.app_context():
        top = ReportRepository.get_top_services(limit=5)
        assert len(top["labels"]) == 2
        assert top["labels"][0] == "Dry Cleaning"
        assert top["data"][0] == 100.0


def test_report_repository_revenue_report_data(app, setup_data):
    with app.app_context():
        res = ReportRepository.get_revenue_report_data(payment_method="Cash")
        assert res["total_revenue"] == 100.0
        assert len(res["payments"]) == 1
        assert res["by_method"]["Cash"] == 100.0


def test_dashboard_service(app, setup_data):
    with app.app_context():
        data = DashboardService.get_dashboard_data()
        assert "kpis" in data
        assert "revenue_trend" in data
        assert "order_status_dist" in data
        assert "top_services" in data
        assert len(data["recent_orders"]) == 2


def test_report_service_revenue_export_csv(app, setup_data):
    with app.app_context():
        csv_str = ReportService.export_revenue_csv()
        assert "Payment Reference,Order Number,Customer Name,Payment Method" in csv_str
        assert "PAY-2026-00001" in csv_str
        assert "100.00" in csv_str


def test_report_service_customer_export_csv(app, setup_data):
    with app.app_context():
        csv_str = ReportService.export_customers_csv()
        assert "Customer Code,Full Name,Phone Number,Total Orders,Total Spent" in csv_str
        assert "CUST-2026-00001" in csv_str
        assert "John Doe" in csv_str


def test_dashboard_route_authenticated(client, setup_data):
    client.post('/auth/login', data={'email': 'admin@test.com', 'password': 'AdminPass123!'})
    response = client.get('/')
    assert response.status_code == 200
    assert b"Dashboard Overview" in response.data
    assert b"Today's Revenue" in response.data


def test_reports_routes_rbac(client, setup_data):
    # 1. Unauthenticated -> Redirect to login
    res_unauth = client.get('/reports/')
    assert res_unauth.status_code == 302
    assert '/auth/login' in res_unauth.location

    # 2. Cashier -> Redirected with permission error
    client.post('/auth/login', data={'email': 'cashier@test.com', 'password': 'CashierPass123!'})
    res_cashier = client.get('/reports/', follow_redirects=True)
    assert b"do not have permission" in res_cashier.data

    # Logout cashier
    client.get('/auth/logout')

    # 3. Admin -> Allowed (200)
    client.post('/auth/login', data={'email': 'admin@test.com', 'password': 'AdminPass123!'})
    res_admin = client.get('/reports/')
    assert res_admin.status_code == 200
    assert b"Reports Central Portal" in res_admin.data

    res_rev = client.get('/reports/revenue')
    assert res_rev.status_code == 200
    assert b"Revenue &amp; Financial Report" in res_rev.data or b"Revenue & Financial Report" in res_rev.data

    res_csv = client.get('/reports/revenue/export-csv')
    assert res_csv.status_code == 200
    assert res_csv.mimetype == 'text/csv'

    res_cust = client.get('/reports/customers')
    assert res_cust.status_code == 200
    assert b"Customer Spending &amp; Activity Analytics" in res_cust.data or b"Customer Spending & Activity Analytics" in res_cust.data

    res_print = client.get('/reports/print')
    assert res_print.status_code == 200
    assert b"Management Summary Report" in res_print.data
