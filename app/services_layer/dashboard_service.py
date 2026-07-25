"""
DashboardService handling business logic for System Dashboard and Analytics.
"""

from app.repositories.report_repository import ReportRepository
from app.repositories.order_repository import OrderRepository
from app.repositories.payment_repository import PaymentRepository


class DashboardService:
    """Service class providing structured dashboard KPI and analytics datasets."""

    @staticmethod
    def get_dashboard_data():
        """
        Compiles high-level system dashboard data including KPIs, Chart.js structures, and recent activity.
        Returns:
            dict: kpis, revenue_trend, order_status_dist, top_services, recent_orders, recent_payments
        """
        kpis = ReportRepository.get_kpi_summary()
        revenue_trend = ReportRepository.get_monthly_revenue_trend(months=6)
        order_status_dist = ReportRepository.get_order_status_distribution()
        top_services = ReportRepository.get_top_services(limit=5)

        # Recent Orders (last 5)
        orders_pagination = OrderRepository.filter_orders(page=1, per_page=5)
        recent_orders = orders_pagination.items if orders_pagination else []

        # Recent Payments (last 5)
        payments_pagination = PaymentRepository.filter_payments(page=1, per_page=5)
        recent_payments = payments_pagination.items if payments_pagination else []

        return {
            'kpis': kpis,
            'revenue_trend': revenue_trend,
            'order_status_dist': order_status_dist,
            'top_services': top_services,
            'recent_orders': recent_orders,
            'recent_payments': recent_payments
        }
