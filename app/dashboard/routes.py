"""
Dashboard blueprint module for KleanFlow Analytics and System Overview.
"""

from flask import Blueprint, render_template
from flask_login import login_required
from app.services_layer.dashboard_service import DashboardService

dashboard_bp = Blueprint('dashboard', __name__)


@dashboard_bp.route('/')
@dashboard_bp.route('/dashboard')
@login_required
def index():
    """Renders main system overview dashboard with KPIs, Chart.js metrics, and recent activity (protected)."""
    dashboard_data = DashboardService.get_dashboard_data()
    return render_template('dashboard.html', **dashboard_data)
