import pytest
from app import create_app
from app.extensions import db
from app.models import User, Customer, Service, Order, OrderItem, Payment, Receipt
from app.services_layer.customer_service import CustomerService
from app.services_layer.order_service import OrderService
from app.services_layer.payment_service import PaymentService
from app.services_layer.report_service import ReportService
from app.services_layer.dashboard_service import DashboardService


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
def setup_environment(app):
    admin = User(full_name="Staff Operator", email="operator@kleanflow.com", phone_number="0205555555", role="Administrator", status="Active")
    admin.set_password("OperatorPass123!")
    db.session.add(admin)
    db.session.commit()

    service1 = Service(service_name="Suit Dry Clean", category="Dry Cleaning", price=60.00, status="Active")
    service2 = Service(service_name="Shirt Wash & Iron", category="Wash & Fold", price=25.00, status="Active")
    db.session.add_all([service1, service2])
    db.session.commit()

    return {"admin": admin, "service1": service1, "service2": service2}


class TestFullEndToEndWorkflows:
    def test_complete_laundry_business_lifecycle(self, app, setup_environment):
        """
        Tests complete lifecycle:
        1. Register Customer
        2. Create Multi-Item Order
        3. Advance Order Status
        4. Record Partial & Final Payments
        5. Verify Auto-Generated Receipts
        6. Verify Dashboard & Reports Metrics
        """
        with app.app_context():
            admin = setup_environment["admin"]
            s1 = setup_environment["service1"]
            s2 = setup_environment["service2"]

            # Step 1: Register Customer
            cust_data = {
                'full_name': 'Ama Serwaa',
                'phone_number': '0248888888',
                'email': 'ama@example.com',
                'address': 'Airport Residential Area, Accra'
            }
            customer, errors = CustomerService.create_customer(cust_data)
            assert errors is None or len(errors) == 0
            assert customer.id is not None
            assert customer.customer_code.startswith("CUST-")

            # Step 2: Create Order (2 Suits @ GH₵60 + 2 Shirts @ GH₵25 = GH₵170 total)
            order_payload = {
                'customer_id': customer.id,
                'items': [
                    {'service_id': s1.id, 'quantity': 2},
                    {'service_id': s2.id, 'quantity': 2}
                ]
            }
            order, o_errors = OrderService.create_order(order_payload, user_id=admin.id)
            assert o_errors is None or len(o_errors) == 0
            assert float(order.total_amount) == 170.00
            assert float(order.balance) == 170.00
            assert order.payment_status == "Unpaid"
            assert order.order_status == "Pending"

            # Step 3: Advance Order Workflow (Pending -> Received -> Washing -> Ironing -> Ready for Pickup)
            OrderService.update_order_status(order.id, "Received", user_id=admin.id)
            OrderService.update_order_status(order.id, "Washing", user_id=admin.id)
            OrderService.update_order_status(order.id, "Ironing", user_id=admin.id)
            OrderService.update_order_status(order.id, "Ready for Pickup", user_id=admin.id)
            
            refreshed_order = OrderService.get_order(order.id)
            assert refreshed_order.order_status == "Ready for Pickup"

            # Step 4: Record Partial Payment (GH₵70)
            pay1_data = {
                'order_id': order.id,
                'amount': 70.00,
                'payment_method': 'Mobile Money'
            }
            payment1, receipt1, p1_errors = PaymentService.record_payment(pay1_data, received_by_id=admin.id)
            assert p1_errors is None or len(p1_errors) == 0
            assert receipt1 is not None
            assert receipt1.receipt_number.startswith("REC-")
            assert float(order.paid_amount) == 70.00
            assert float(order.balance) == 100.00
            assert order.payment_status == "Partial"

            # Step 5: Record Final Payment (GH₵100)
            pay2_data = {
                'order_id': order.id,
                'amount': 100.00,
                'payment_method': 'Cash'
            }
            payment2, receipt2, p2_errors = PaymentService.record_payment(pay2_data, received_by_id=admin.id)
            assert p2_errors is None or len(p2_errors) == 0
            assert float(order.paid_amount) == 170.00
            assert float(order.balance) == 0.00
            assert order.payment_status == "Paid"

            # Complete order
            OrderService.update_order_status(order.id, "Completed", user_id=admin.id)

            # Step 6: Verify Dashboard & Reports Integration
            db_data = DashboardService.get_dashboard_data()
            assert db_data['kpis']['today_revenue'] == 170.00
            assert db_data['kpis']['monthly_revenue'] == 170.00
            assert db_data['kpis']['unpaid_balance'] == 0.00

            rev_report = ReportService.generate_revenue_report()
            assert rev_report['total_revenue'] == 170.00
            assert rev_report['total_transactions'] == 2
            assert rev_report['by_method']['Mobile Money'] == 70.00
            assert rev_report['by_method']['Cash'] == 100.00

            cust_report = ReportService.generate_customer_report()
            assert len(cust_report) == 1
            assert cust_report[0]['customer'].id == customer.id
            assert cust_report[0]['total_spent'] == 170.00
            assert cust_report[0]['total_balance'] == 0.00


class TestOrderCancellationIntegration:
    def test_order_cancellation_payment_guard(self, app, setup_environment):
        """Verifies cancelled order rejects further payment processing."""
        with app.app_context():
            admin = setup_environment["admin"]
            s1 = setup_environment["service1"]

            customer, _ = CustomerService.create_customer({'full_name': 'Kofi Badu', 'phone_number': '0209998877', 'address': 'Tema'})
            order, _ = OrderService.create_order({'customer_id': customer.id, 'items': [{'service_id': s1.id, 'quantity': 1}]}, user_id=admin.id)

            # Cancel Order
            cancelled_order, c_errors = OrderService.cancel_order(order.id, user_id=admin.id)
            assert c_errors is None or len(c_errors) == 0
            assert cancelled_order.order_status == "Cancelled"

            # Attempt Payment on Cancelled Order
            _, _, p_errors = PaymentService.record_payment({'order_id': order.id, 'amount': 60.00, 'payment_method': 'Cash'}, received_by_id=admin.id)
            assert p_errors is not None and len(p_errors) > 0
            assert any("cancelled" in err.lower() for err in p_errors)
