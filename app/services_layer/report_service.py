"""
ReportService handling revenue analytics, customer reports, and CSV export logic.
"""

import io
import csv
from datetime import datetime, date
from app.repositories.report_repository import ReportRepository


class ReportService:
    """Service class for reporting analytics and CSV exports."""

    @staticmethod
    def generate_revenue_report(start_date=None, end_date=None, payment_method=None):
        """
        Generates revenue analytics dataset based on date range and payment method filters.
        """
        return ReportRepository.get_revenue_report_data(
            start_date=start_date,
            end_date=end_date,
            payment_method=payment_method
        )

    @staticmethod
    def generate_customer_report(limit=50):
        """
        Generates customer leaderboard report ordered by total expenditure in GH₵.
        """
        return ReportRepository.get_customer_spending_report(limit=limit)

    @staticmethod
    def export_revenue_csv(start_date=None, end_date=None, payment_method=None):
        """
        Formats revenue payment transactions into a downloadable CSV string.
        Returns:
            str: CSV formatted string content
        """
        report_data = ReportRepository.get_revenue_report_data(
            start_date=start_date,
            end_date=end_date,
            payment_method=payment_method
        )

        output = io.StringIO()
        writer = csv.writer(output)

        # Header Row
        writer.writerow([
            'Payment Reference',
            'Order Number',
            'Customer Name',
            'Customer Phone',
            'Payment Method',
            'Amount Paid (GH₵)',
            'Transaction Date'
        ])

        # Data Rows
        for payment in report_data['payments']:
            customer_name = payment.order.customer.full_name if payment.order and payment.order.customer else 'N/A'
            customer_phone = payment.order.customer.phone_number if payment.order and payment.order.customer else 'N/A'
            order_number = payment.order.order_number if payment.order else 'N/A'

            writer.writerow([
                payment.payment_reference,
                order_number,
                customer_name,
                customer_phone,
                payment.payment_method,
                f"{payment.amount:.2f}",
                payment.created_at.strftime('%Y-%m-%d %H:%M') if payment.created_at else 'N/A'
            ])

        return output.getvalue()

    @staticmethod
    def export_customers_csv(limit=100):
        """
        Formats customer spending report into a downloadable CSV string.
        Returns:
            str: CSV formatted string content
        """
        customers_data = ReportRepository.get_customer_spending_report(limit=limit)

        output = io.StringIO()
        writer = csv.writer(output)

        # Header Row
        writer.writerow([
            'Customer Code',
            'Full Name',
            'Phone Number',
            'Email',
            'Total Orders',
            'Total Spent (GH₵)',
            'Outstanding Balance (GH₵)'
        ])

        # Data Rows
        for item in customers_data:
            c = item['customer']
            writer.writerow([
                c.customer_code,
                c.full_name,
                c.phone_number,
                c.email or 'N/A',
                item['total_orders'],
                f"{item['total_spent']:.2f}",
                f"{item['total_balance']:.2f}"
            ])

        return output.getvalue()
