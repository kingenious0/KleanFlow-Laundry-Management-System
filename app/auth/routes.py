"""
Authentication Blueprint Routes for KleanFlow.
"""

from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.services_layer.auth_service import AuthService
from app.services_layer.user_service import UserService

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Renders login page and handles authentication requests."""
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.index'))

    if request.method == 'POST':
        email = request.form.get('email', '')
        password = request.form.get('password', '')
        remember = bool(request.form.get('remember'))

        user, error = AuthService.authenticate_user(email, password)
        if error:
            flash(error, 'danger')
            return render_template('login.html', email=email)

        AuthService.login_session(user, remember=remember)
        flash(f"Welcome back, {user.full_name}!", "success")

        next_page = request.args.get('next')
        if next_page and next_page.startswith('/'):
            return redirect(next_page)
        return redirect(url_for('dashboard.index'))

    return render_template('login.html')


@auth_bp.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    """Logs current user out of session."""
    AuthService.logout_session()
    flash("You have been successfully logged out.", "info")
    return redirect(url_for('auth.login'))


@auth_bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    """User self-service profile page."""
    if request.method == 'POST':
        action = request.form.get('action')

        if action == 'update_profile':
            data = {
                'full_name': request.form.get('full_name', ''),
                'email': current_user.email,  # Email remains static on self profile
                'phone_number': request.form.get('phone_number', ''),
                'role': current_user.role,
                'status': current_user.status
            }
            updated_user, errors = UserService.update_user(current_user.id, data)
            if errors:
                for err in errors:
                    flash(err, 'danger')
            else:
                flash("Profile details updated successfully.", "success")
                return redirect(url_for('auth.profile'))

        elif action == 'change_password':
            current_pwd = request.form.get('current_password', '')
            new_pwd = request.form.get('new_password', '')
            confirm_pwd = request.form.get('confirm_password', '')

            if new_pwd != confirm_pwd:
                flash("New password and password confirmation do not match.", "danger")
            else:
                success, error = UserService.change_password(current_user.id, current_pwd, new_pwd)
                if success:
                    flash("Password changed successfully.", "success")
                    return redirect(url_for('auth.profile'))
                else:
                    flash(error, "danger")

    return render_template('users/profile.html')
