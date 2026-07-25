import pytest
from app import create_app
from app.extensions import db
from app.models.user import User
from app.models.customer import Customer
from app.models.service import Service
from app.models.order import Order
from app.models.order_item import OrderItem
from app.models.payment import Payment
from app.models.receipt import Receipt
from app.services_layer.payment_service import PaymentService
from app.services_layer.receipt_service import ReceiptService


@pytest.fixture
def app():
    """Create test application instance."""
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
    """Test client instance."""
    return app.test_client()


@pytest.fixture
def test_setup(app):
    """Fixture providing test user, customer, service, and order."""
    with app.app_context():
        # Create Cashier User
        cashier = User(
            full_name='Test Cashier',
            email='cashier@kleanflow.com',
            phone_number='0240000099',
            role='Cashier',
            status='Active'
        )
        cashier.set_password('Password123!')

        # Create Customer
        customer = Customer(
            customer_code='CUST-0001',
            full_name='Kofi Mensah',
            phone_number='0244123456',
            address='Accra Central',
            is_active=True
        )

        # Create Service
        service = Service(
            name='Suit Washing & Pressing',
            category='Dry Cleaning',
            price=50.00,
            is_active=True
        )

        db.session.add_all([cashier, customer, service])
        db.session.commit()

        # Create Order with total GH₵ 100.00 (2 x 50.00)
        order = Order(
            order_number='KF-2026-00001',
            customer_id=customer.id,
            created_by=cashier.id,
            total_amount=100.00,
            paid_amount=0.00,
            balance=100.00,
            payment_status='Unpaid',
            order_status='Pending'
        )
        db.session.add(order)
        db.session.commit()

        item = OrderItem(
            order_id=order.id,
            service_id=service.id,
            quantity=2,
            unit_price=50.00,
            subtotal=100.00
        )
        db.session.add(item)
        db.session.commit()

        return {
            'cashier_id': cashier.id,
            'customer_id': customer.id,
            'service_id': service.id,
            'order_id': order.id
        }


def test_record_payment_success_full_payment(app, test_setup):
    """Test recording a full payment of GH₵ 100.00."""
    with app.app_context():
        payment, error = PaymentService.process_payment(
            order_id=test_setup['order_id'],
            amount=100.00,
            payment_method='Cash',
            received_by=test_setup['cashier_id']
        )

        assert error is None
        assert payment is not None
        assert payment.payment_reference.startswith('PAY-')
        assert payment.amount == 100.00
        assert payment.payment_method == 'Cash'

        # Verify Order balance and payment status update
        order = db.session.get(Order, test_setup['order_id'])
        assert order.paid_amount == 100.00
        assert order.balance == 0.00
        assert order.payment_status == 'Paid'

        # Verify Auto Receipt creation (BR-REC-001)
        receipt = db.session.query(Receipt).filter_by(payment_id=payment.id).first()
        assert receipt is not None
        assert receipt.receipt_number.startswith('REC-')
        assert receipt.amount_paid == 100.00


def test_record_payment_partial_payment(app, test_setup):
    """Test recording partial payment followed by remaining balance."""
    with app.app_context():
        # First partial payment: GH₵ 40.00
        payment1, error1 = PaymentService.process_payment(
            order_id=test_setup['order_id'],
            amount=40.00,
            payment_method='Mobile Money',
            received_by=test_setup['cashier_id']
        )
        assert error1 is None
        order = db.session.get(Order, test_setup['order_id'])
        assert order.paid_amount == 40.00
        assert order.balance == 60.00
        assert order.payment_status == 'Partially Paid'

        # Second payment: GH₵ 60.00
        payment2, error2 = PaymentService.process_payment(
            order_id=test_setup['order_id'],
            amount=60.00,
            payment_method='Cash',
            received_by=test_setup['cashier_id']
        )
        assert error2 is None
        order = db.session.get(Order, test_setup['order_id'])
        assert order.paid_amount == 100.00
        assert order.balance == 0.00
        assert order.payment_status == 'Paid'


def test_record_payment_excess_amount_fails(app, test_setup):
    """Test that paying more than order balance fails per BR-PAY-002."""
    with app.app_context():
        payment, error = PaymentService.process_payment(
            order_id=test_setup['order_id'],
            amount=150.00,  # Max is 100.00
            payment_method='Cash',
            received_by=test_setup['cashier_id']
        )
        assert payment is None
        assert error is not None
        assert 'exceeds remaining balance' in error.lower()


def test_record_payment_zero_or_negative_fails(app, test_setup):
    """Test that zero or negative payment amount fails per BR-PAY-002."""
    with app.app_context():
        payment, error = PaymentService.process_payment(
            order_id=test_setup['order_id'],
            amount=0.00,
            payment_method='Cash',
            received_by=test_setup['cashier_id']
        )
        assert payment is None
        assert 'must be greater than zero' in error.lower()


def test_record_payment_invalid_method_fails(app, test_setup):
    """Test that invalid payment method fails validation."""
    with app.app_context():
        payment, error = PaymentService.process_payment(
            order_id=test_setup['order_id'],
            amount=50.00,
            payment_method='Cryptocurrency',
            received_by=test_setup['cashier_id']
        )
        assert payment is None
        assert 'invalid payment method' in error.lower()


def test_record_payment_cancelled_order_fails(app, test_setup):
    """Test that payments cannot be recorded for cancelled orders."""
    with app.app_context():
        order = db.session.get(Order, test_setup['order_id'])
        order.order_status = 'Cancelled'
        db.session.commit()

        payment, error = PaymentService.process_payment(
            order_id=test_setup['order_id'],
            amount=50.00,
            payment_method='Cash',
            received_by=test_setup['cashier_id']
        )
        assert payment is None
        assert 'cannot record payment for a cancelled order' in error.lower()


def test_receipt_printable_data(app, test_setup):
    """Test formatting printable receipt dataset per BR-REC-002."""
    with app.app_context():
        payment, _ = PaymentService.process_payment(
            order_id=test_setup['order_id'],
            amount=100.00,
            payment_method='Cash',
            received_by=test_setup['cashier_id']
        )
        receipt = db.session.query(Receipt).filter_by(payment_id=payment.id).first()

        data = ReceiptService.get_printable_receipt_data(receipt.id)
        assert data is not None
        assert data['receipt_number'] == receipt.receipt_number
        assert data['customer']['name'] == 'Kofi Mensah'
        assert data['payment']['amount'] == 100.00
        assert data['order']['total_amount'] == 100.00
        assert len(data['order']['items']) == 1
        assert data['order']['items'][0]['service_name'] == 'Suit Washing & Pressing'


def test_payments_routes_access(client, app, test_setup):
    """Test HTTP routes for payments with auth and CSRF disabled."""
    # Login as cashier
    client.post('/auth/login', data={
        'email': 'cashier@kleanflow.com',
        'password': 'Password123!'
    })

    # Get payments index page
    res_index = client.get('/payments/')
    assert res_index.status_code == 200
    assert b'Payments History' in res_index.data

    # Record payment via POST
    res_post = client.post('/payments/record', data={
        'order_id': test_setup['order_id'],
        'amount': '50.00',
        'payment_method': 'Cash'
    }, follow_redirects=True)

    assert res_post.status_code == 200
    assert b'Payment of GH\xc2\xa2 50.00 recorded successfully' in res_post.data or b'recorded successfully' in res_post.data

    # Get receipts index page
    res_receipts = client.get('/receipts/')
    assert res_receipts.status_code == 200
    assert b'Receipts' in res_receipts.data
