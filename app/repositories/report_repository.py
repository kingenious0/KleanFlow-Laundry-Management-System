"""
ReportRepository handling SQL database aggregation queries for Dashboard & Analytics.
"""

from datetime import datetime, date, timedelta
from sqlalchemy import func, extract
from app.extensions import db
from app.models.order import Order
from app.models.payment import Payment
from app.models.customer import Customer
from app.models.service import Service
from app.models.order_item import OrderItem


class ReportRepository:
    """Repository class for statistical aggregations, KPI metrics, and reporting datasets."""

    @staticmethod
    def get_kpi_summary():
        """
        Retrieves high-level Key Performance Indicators for the system dashboard.
        Returns:
            dict: today_revenue, month_revenue, total_orders, unpaid_balance, active_customers
        """
        today_date = date.today()
        current_year = today_date.year
        current_month = today_date.month

        # Today's Revenue (Payments completed today)
        today_revenue = db.session.query(
            func.coalesce(func.sum(Payment.amount), 0.00)
        ).filter(
            func.date(Payment.payment_date) == today_date,
            Payment.payment_status == 'Completed'
        ).scalar() or 0.00

        # Monthly Revenue (Payments completed this month)
        month_revenue = db.session.query(
            func.coalesce(func.sum(Payment.amount), 0.00)
        ).filter(
            extract('year', Payment.payment_date) == current_year,
            extract('month', Payment.payment_date) == current_month,
            Payment.payment_status == 'Completed'
        ).scalar() or 0.00

        # Total Orders count this month
        month_orders_count = db.session.query(
            func.count(Order.id)
        ).filter(
            extract('year', Order.created_at) == current_year,
            extract('month', Order.created_at) == current_month,
            Order.is_deleted == False
        ).scalar() or 0

        # Total Unpaid Balance across active, non-cancelled orders
        unpaid_balance = db.session.query(
            func.coalesce(func.sum(Order.balance), 0.00)
        ).filter(
            Order.order_status != 'Cancelled',
            Order.balance > 0,
            Order.is_deleted == False
        ).scalar() or 0.00

        # Active Customers count
        active_customers_count = db.session.query(
            func.count(Customer.id)
        ).filter(
            Customer.is_deleted == False
        ).scalar() or 0

        return {
            'today_revenue': float(today_revenue),
            'monthly_revenue': float(month_revenue),
            'orders_count_month': int(month_orders_count),
            'unpaid_balance': float(unpaid_balance),
            'active_customers': int(active_customers_count)
        }

    @staticmethod
    def get_monthly_revenue_trend(months=6):
        """
        Retrieves monthly revenue totals for the past N months for Chart.js line graph.
        Returns:
            dict: {'labels': ['Feb 2026', ...], 'data': [100.0, ...]}
        """
        labels = []
        data = []
        today = date.today()

        for i in range(months - 1, -1, -1):
            # Calculate target year and month
            target_date = today.replace(day=1) - timedelta(days=i * 30)
            target_year = target_date.year
            target_month = target_date.month
            month_name = target_date.strftime('%b %Y')

            revenue = db.session.query(
                func.coalesce(func.sum(Payment.amount), 0.00)
            ).filter(
                extract('year', Payment.payment_date) == target_year,
                extract('month', Payment.payment_date) == target_month,
                Payment.payment_status == 'Completed'
            ).scalar() or 0.00

            labels.append(month_name)
            data.append(float(revenue))

        return {
            'labels': labels,
            'data': data
        }

    @staticmethod
    def get_order_status_distribution():
        """
        Retrieves count of orders per status for Chart.js doughnut chart.
        Returns:
            dict: {'labels': [...], 'data': [...]}
        """
        statuses = ['Pending', 'Ready for Pickup', 'Completed', 'In Progress', 'Cancelled']
        query_results = db.session.query(
            Order.order_status,
            func.count(Order.id)
        ).filter(
            Order.is_deleted == False
        ).group_by(Order.order_status).all()

        status_dict = {status: count for status, count in query_results}
        
        labels = []
        data = []
        for status in statuses:
            if status in status_dict:
                labels.append(status)
                data.append(status_dict[status])

        return {
            'labels': labels,
            'data': data
        }

    @staticmethod
    def get_top_services(limit=5):
        """
        Retrieves top performing laundry services by order volume & revenue.
        Returns:
            dict: {'labels': [...], 'data': [...]}
        """
        query_results = db.session.query(
            Service.service_name,
            func.sum(OrderItem.subtotal).label('total_revenue')
        ).join(
            OrderItem, Service.id == OrderItem.service_id
        ).join(
            Order, OrderItem.order_id == Order.id
        ).filter(
            Order.order_status != 'Cancelled',
            Order.is_deleted == False
        ).group_by(
            Service.service_name
        ).order_by(
            func.sum(OrderItem.subtotal).desc()
        ).limit(limit).all()

        labels = [name for name, rev in query_results]
        data = [float(rev or 0.0) for name, rev in query_results]

        return {
            'labels': labels,
            'data': data
        }

    @staticmethod
    def get_revenue_report_data(start_date=None, end_date=None, payment_method=None):
        """
        Retrieves filtered payment transactions dataset for revenue reporting.
        """
        query = Payment.query.join(Order).filter(Payment.payment_status == 'Completed')

        if start_date:
            query = query.filter(func.date(Payment.payment_date) >= start_date)
        if end_date:
            query = query.filter(func.date(Payment.payment_date) <= end_date)
        if payment_method and payment_method != 'All':
            query = query.filter(Payment.payment_method == payment_method)

        payments = query.order_by(Payment.payment_date.desc()).all()

        total_collected = sum(float(p.amount) for p in payments)

        # Breakdown by method
        method_totals = {'Cash': 0.0, 'Mobile Money': 0.0, 'Card': 0.0, 'Bank Transfer': 0.0}
        for p in payments:
            if p.payment_method in method_totals:
                method_totals[p.payment_method] += float(p.amount)

        return {
            'payments': payments,
            'total_revenue': total_collected,
            'by_method': method_totals,
            'total_transactions': len(payments)
        }

    @staticmethod
    def get_customer_spending_report(limit=20):
        """
        Retrieves customer leaderboard ranked by total expenditure (GH₵).
        """
        results = db.session.query(
            Customer,
            func.count(Order.id).label('total_orders'),
            func.coalesce(func.sum(Order.paid_amount), 0.00).label('total_spent'),
            func.coalesce(func.sum(Order.paid_amount), 0.00).label('total_paid'),
            func.coalesce(func.sum(Order.balance), 0.00).label('total_balance')
        ).join(
            Order, Customer.id == Order.customer_id
        ).filter(
            Customer.is_deleted == False,
            Order.is_deleted == False,
            Order.order_status != 'Cancelled'
        ).group_by(
            Customer.id
        ).order_by(
            func.sum(Order.paid_amount).desc()
        ).limit(limit).all()

        output = []
        for customer, order_count, spent, paid, balance in results:
            output.append({
                'customer': customer,
                'orders_count': int(order_count),
                'total_spent': float(spent),
                'total_paid': float(paid),
                'total_balance': float(balance)
            })
        return output
