"""
User Management Blueprint Routes for KleanFlow.
"""

from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import current_user
from app.decorators.auth_decorators import admin_required, roles_required
from app.services_layer.user_service import UserService
from app.validators.user_validator import VALID_ROLES, VALID_STATUSES

users_bp = Blueprint('users', __name__, url_prefix='/users')


@users_bp.route('/', methods=['GET'])
@roles_required('Manager')
def index():
    """Renders user management dashboard table with search and pagination."""
    search_query = request.args.get('search', '').strip()
    role_filter = request.args.get('role', '').strip()
    status_filter = request.args.get('status', '').strip()
    page = request.args.get('page', 1, type=int)

    pagination = UserService.list_users(
        search_query=search_query,
        role=role_filter if role_filter in VALID_ROLES else None,
        status=status_filter if status_filter in VALID_STATUSES else None,
        page=page,
        per_page=10
    )

    return render_template(
        'users/index.html',
        pagination=pagination,
        users=pagination.items,
        search=search_query,
        selected_role=role_filter,
        selected_status=status_filter,
        roles=VALID_ROLES,
        statuses=VALID_STATUSES
    )


@users_bp.route('/create', methods=['GET', 'POST'])
@admin_required
def create():
    """Renders user creation form and handles new user submission."""
    if request.method == 'POST':
        data = {
            'full_name': request.form.get('full_name', ''),
            'email': request.form.get('email', ''),
            'phone_number': request.form.get('phone_number', ''),
            'password': request.form.get('password', ''),
            'role': request.form.get('role', 'Laundry Attendant'),
            'status': request.form.get('status', 'Active')
        }

        created_user, errors = UserService.create_user(data)
        if errors:
            for err in errors:
                flash(err, 'danger')
            return render_template('users/create.html', data=data, roles=VALID_ROLES, statuses=VALID_STATUSES)

        flash(f"User account for '{created_user.full_name}' created successfully.", "success")
        return redirect(url_for('users.index'))

    return render_template('users/create.html', roles=VALID_ROLES, statuses=VALID_STATUSES)


@users_bp.route('/<int:user_id>/edit', methods=['GET', 'POST'])
@admin_required
def edit(user_id):
    """Renders user edit form and updates existing user details."""
    target_user = UserService.get_user_by_id(user_id)
    if not target_user:
        flash("User not found.", "danger")
        return redirect(url_for('users.index'))

    if request.method == 'POST':
        data = {
            'full_name': request.form.get('full_name', ''),
            'email': request.form.get('email', ''),
            'phone_number': request.form.get('phone_number', ''),
            'role': request.form.get('role', target_user.role),
            'status': request.form.get('status', target_user.status),
            'password': request.form.get('password', '')
        }

        updated_user, errors = UserService.update_user(user_id, data, current_user_id=current_user.id)
        if errors:
            for err in errors:
                flash(err, 'danger')
            return render_template('users/edit.html', user=target_user, data=data, roles=VALID_ROLES, statuses=VALID_STATUSES)

        flash(f"User account '{updated_user.full_name}' updated successfully.", "success")
        return redirect(url_for('users.index'))

    return render_template('users/edit.html', user=target_user, roles=VALID_ROLES, statuses=VALID_STATUSES)


@users_bp.route('/<int:user_id>/toggle-status', methods=['POST'])
@admin_required
def toggle_status(user_id):
    """Toggles active/inactive status of specified user."""
    success, message = UserService.toggle_user_status(user_id, current_user_id=current_user.id)
    if success:
        flash(message, "success")
    else:
        flash(message, "danger")
    return redirect(url_for('users.index'))


@users_bp.route('/<int:user_id>/delete', methods=['POST'])
@admin_required
def delete(user_id):
    """Deletes specified user account."""
    success, message = UserService.delete_user(user_id, current_user_id=current_user.id)
    if success:
        flash(message, "success")
    else:
        flash(message, "danger")
    return redirect(url_for('users.index'))
