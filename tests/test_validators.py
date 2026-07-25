import pytest
from app import create_app
from app.extensions import db
from app.models import User, Customer, Service, Order, OrderItem
from app.validators.user_validator import UserValidator
from app.validators.customer_validator import CustomerValidator
from app.validators.service_validator import ServiceValidator
from app.validators.order_validator import OrderValidator
from app.validators.payment_validator import PaymentValidator


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


class TestUserValidator:
    def test_validate_email_format(self):
        assert UserValidator.validate_email_format("test@example.com") is True
        assert UserValidator.validate_email_format("invalid-email") is False
        assert UserValidator.validate_email_format("") is False
        assert UserValidator.validate_email_format(None) is False

    def test_validate_password_strength(self):
        # Valid password
        errors = UserValidator.validate_password_strength("StrongPass123!")
        assert len(errors) == 0

        # Short password
        errors = UserValidator.validate_password_strength("Short1!")
        assert any("at least 8 characters" in e for e in errors)

        # No uppercase
        errors = UserValidator.validate_password_strength("password123!")
        assert any("uppercase" in e for e in errors)

        # No lowercase
        errors = UserValidator.validate_password_strength("PASSWORD123!")
        assert any("lowercase" in e for e in errors)

        # No number
        errors = UserValidator.validate_password_strength("Password!")
        assert any("number" in e for e in errors)

        # No special character
        errors = UserValidator.validate_password_strength("Password123")
        assert any("special character" in e for e in errors)

    def test_validate_user_creation_duplicate_email(self, app):
        user = User(full_name="Existing User", email="exist@example.com", phone_number="0241111111", role="Cashier")
        user.set_password("Password123!")
        db.session.add(user)
        db.session.commit()

        data = {
            'full_name': 'New User',
            'email': 'exist@example.com',
            'phone_number': '0242222222',
            'password': 'Password123!',
            'role': 'Cashier'
        }
        errors = UserValidator.validate_user_creation(data)
        assert any("already exists" in e for e in errors)


class TestCustomerValidator:
    def test_validate_phone_format(self):
        assert CustomerValidator.validate_phone_format("0241234567") is True
        assert CustomerValidator.validate_phone_format("+233241234567") is True
        assert CustomerValidator.validate_phone_format("12345") is False
        assert CustomerValidator.validate_phone_format("") is False

    def test_validate_customer_creation_missing_fields(self):
        data = {'full_name': '', 'phone_number': '', 'address': ''}
        errors = CustomerValidator.validate_customer_creation(data)
        assert any("full name is required" in e for e in errors)
        assert any("Phone number is required" in e for e in errors)
        assert any("address is required" in e for e in errors)


class TestServiceValidator:
    def test_validate_service_creation_negative_price(self, app):
        data = {
            'service_name': 'Pressing Only',
            'category': 'Ironing & Pressing',
            'price': -15.00,
            'status': 'Active'
        }
        errors = ServiceValidator.validate_service_creation(data)
        assert any("cannot be negative" in e for e in errors)

    def test_validate_service_creation_invalid_status(self, app):
        data = {
            'service_name': 'Dry Cleaning Premium',
            'category': 'Dry Cleaning',
            'price': 40.00,
            'status': 'UnknownStatus'
        }
        errors = ServiceValidator.validate_service_creation(data)
        assert any("Status must be one of" in e for e in errors)


class TestOrderValidator:
    def test_validate_order_creation_empty_items(self, app):
        customer = Customer(customer_code="CUST-001", full_name="Test Customer", phone_number="0240000000", address="Accra")
        db.session.add(customer)
        db.session.commit()

        data = {'customer_id': customer.id, 'items': []}
        errors = OrderValidator.validate_order_creation(data)
        assert any("at least one service item" in e for e in errors)

    def test_validate_order_creation_inactive_service(self, app):
        customer = Customer(customer_code="CUST-002", full_name="Test Customer 2", phone_number="0240000001", address="Accra")
        service = Service(service_name="Discontinued Wash", category="General", price=10.0, status="Inactive")
        db.session.add_all([customer, service])
        db.session.commit()

        data = {
            'customer_id': customer.id,
            'items': [{'service_id': service.id, 'quantity': 2}]
        }
        errors = OrderValidator.validate_order_creation(data)
        assert any("currently inactive" in e for e in errors)


class TestPaymentValidator:
    def test_validate_payment_recording_overpayment(self, app):
        customer = Customer(customer_code="CUST-003", full_name="Test Customer 3", phone_number="0240000002", address="Accra")
        order = Order(order_number="ORD-TEST-001", customer_id=1, total_amount=100.0, paid_amount=50.0, balance=50.0, payment_status="Partial")
        db.session.add_all([customer, order])
        db.session.commit()

        data = {
            'order_id': order.id,
            'amount': 75.00,
            'payment_method': 'Cash'
        }
        errors = PaymentValidator.validate_payment_recording(data)
        assert any("cannot exceed remaining balance" in e for e in errors)

    def test_validate_payment_recording_negative_amount(self, app):
        order = Order(order_number="ORD-TEST-002", customer_id=1, total_amount=100.0, paid_amount=0.0, balance=100.0)
        db.session.add(order)
        db.session.commit()

        data = {
            'order_id': order.id,
            'amount': -10.00,
            'payment_method': 'Cash'
        }
        errors = PaymentValidator.validate_payment_recording(data)
        assert any("greater than zero" in e for e in errors)
