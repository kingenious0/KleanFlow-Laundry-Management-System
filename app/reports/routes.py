"""
Reports blueprint module for KleanFlow system reporting and CSV exports.
"""

from datetime import datetime, date
from flask import Blueprint, render_template, request, Response, flash, redirect, url_for
from flask_login import login_required
from app.decorators.auth_decorators import roles_required
from app.services_layer.report_service import ReportService
from app.services_layer.dashboard_service import DashboardService

reports_bp = Blueprint('reports', __name__, url_prefix='/reports')


@reports_bp.route('/')
@login_required
@roles_required('Administrator', 'Manager')
def index():
    """Renders main reports overview portal."""
    return render_template('reports/index.html')


@reports_bp.route('/revenue', methods=['GET'])
@login_required
@roles_required('Administrator', 'Manager')
def revenue_report():
    """Renders revenue report with date range & payment method filtering."""
    start_date_str = request.args.get('start_date', '').strip()
    end_date_str = request.args.get('end_date', '').strip()
    payment_method = request.args.get('payment_method', '').strip()

    start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date() if start_date_str else None
    end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date() if end_date_str else None

    report_data = ReportService.generate_revenue_report(
        start_date=start_date,
        end_date=end_date,
        payment_method=payment_method if payment_method else None
    )

    return render_template(
        'reports/revenue.html',
        total_revenue=report_data['total_revenue'],
        total_transactions=report_data['total_transactions'],
        by_method=report_data['by_method'],
        payments=report_data['payments'],
        start_date=start_date_str,
        end_date=end_date_str,
        selected_method=payment_method
    )


@reports_bp.route('/revenue/export-csv', methods=['GET'])
@login_required
@roles_required('Administrator', 'Manager')
def export_revenue_csv():
    """Exports revenue report dataset as CSV file download."""
    start_date_str = request.args.get('start_date', '').strip()
    end_date_str = request.args.get('end_date', '').strip()
    payment_method = request.args.get('payment_method', '').strip()

    start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date() if start_date_str else None
    end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date() if end_date_str else None

    csv_data = ReportService.export_revenue_csv(
        start_date=start_date,
        end_date=end_date,
        payment_method=payment_method if payment_method else None
    )

    filename = f"KleanFlow_Revenue_Report_{date.today().strftime('%Y%m%d')}.csv"
    return Response(
        csv_data,
        mimetype="text/csv",
        headers={"Content-disposition": f"attachment; filename={filename}"}
    )


@reports_bp.route('/customers', methods=['GET'])
@login_required
@roles_required('Administrator', 'Manager')
def customer_report():
    """Renders customer spending leaderboard report."""
    limit = request.args.get('limit', 50, type=int)
    customers_data = ReportService.generate_customer_report(limit=limit)
    return render_template('reports/customers.html', customer_data=customers_data, limit=limit)


@reports_bp.route('/customers/export-csv', methods=['GET'])
@login_required
@roles_required('Administrator', 'Manager')
def export_customers_csv():
    """Exports customer spending report dataset as CSV file download."""
    limit = request.args.get('limit', 100, type=int)
    csv_data = ReportService.export_customers_csv(limit=limit)
    filename = f"KleanFlow_Customer_Report_{date.today().strftime('%Y%m%d')}.csv"
    return Response(
        csv_data,
        mimetype="text/csv",
        headers={"Content-disposition": f"attachment; filename={filename}"}
    )


@reports_bp.route('/print', methods=['GET'])
@login_required
@roles_required('Administrator', 'Manager')
def print_report():
    """Renders clean printable summary report view per BR-REC-002 / @media print."""
    dashboard_data = DashboardService.get_dashboard_data()
    return render_template(
        'reports/print.html',
        kpis=dashboard_data['kpis'],
        revenue_trend=dashboard_data['revenue_trend'],
        top_services=dashboard_data['top_services'],
        generated_at=datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')
    )
