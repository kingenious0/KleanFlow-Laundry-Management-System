"""
Authentication and Role-Based Access Control (RBAC) Decorators for KleanFlow.
"""

from functools import wraps
from flask import flash, redirect, url_for, request
from flask_login import current_user


def roles_required(*roles):
    """
    Decorator to restrict route access to users with specified role(s).
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated:
                flash("Please log in to access this page.", "warning")
                return redirect(url_for('auth.login', next=request.url))

            if current_user.status != 'Active':
                flash("Your account is inactive. Please contact a manager.", "danger")
                return redirect(url_for('auth.login'))

            if current_user.role not in roles:
                flash("You do not have permission to access this page.", "danger")
                return redirect(url_for('dashboard.index'))

            return f(*args, **kwargs)
        return decorated_function
    return decorator


def admin_required(f):
    """Decorator shortcut for Manager routes."""
    return roles_required('Manager')(f)


def manager_required(f):
    """Decorator shortcut for Manager routes."""
    return roles_required('Manager')(f)
