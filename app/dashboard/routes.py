"""
Dashboard blueprint module for KleanFlow.
"""

from flask import Blueprint, render_template
from flask_login import login_required

dashboard_bp = Blueprint('dashboard', __name__)


@dashboard_bp.route('/')
@dashboard_bp.route('/dashboard')
@login_required
def index():
    """Renders main system overview dashboard (protected)."""
    return render_template('dashboard.html')
