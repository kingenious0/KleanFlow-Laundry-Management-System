"""
Services Blueprint Routes for KleanFlow Laundry Services Management.
"""

from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required
from app.decorators.auth_decorators import roles_required
from app.services_layer.service_service import ServiceService

services_bp = Blueprint('services', __name__, url_prefix='/services')


@services_bp.route('/', methods=['GET'])
@login_required
def index():
    """Renders laundry services list with search, category, and status filters."""
    search_query = request.args.get('search', '').strip()
    category = request.args.get('category', '').strip()
    status = request.args.get('status', '').strip()
    page = request.args.get('page', 1, type=int)

    pagination = ServiceService.list_services(
        search_query=search_query,
        category=category,
        status=status,
        page=page,
        per_page=12
    )

    categories = ServiceService.get_categories()

    return render_template(
        'services/index.html',
        pagination=pagination,
        services=pagination.items,
        categories=categories,
        search=search_query,
        selected_category=category,
        selected_status=status
    )


@services_bp.route('/create', methods=['GET', 'POST'])
@roles_required('Administrator', 'Manager')
def create():
    """Renders new laundry service form and handles creation."""
    categories = ServiceService.get_categories()

    if request.method == 'POST':
        data = {
            'service_name': request.form.get('service_name', ''),
            'category': request.form.get('category', ''),
            'custom_category': request.form.get('custom_category', ''),
            'price': request.form.get('price', ''),
            'description': request.form.get('description', ''),
            'status': request.form.get('status', 'Active')
        }

        # If custom category provided, use it
        if data['category'] == 'NEW' and data['custom_category']:
            data['category'] = data['custom_category']

        created_service, errors = ServiceService.create_service(data)
        if errors:
            for err in errors:
                flash(err, 'danger')
            return render_template('services/create.html', categories=categories, data=data)

        flash(f"Laundry service '{created_service.service_name}' created successfully.", "success")
        return redirect(url_for('services.index'))

    return render_template('services/create.html', categories=categories)


@services_bp.route('/<int:service_id>/edit', methods=['GET', 'POST'])
@roles_required('Administrator', 'Manager')
def edit(service_id):
    """Renders service edit form and handles updates."""
    target_service = ServiceService.get_service_by_id(service_id)
    if not target_service:
        flash("Laundry service not found.", "danger")
        return redirect(url_for('services.index'))

    categories = ServiceService.get_categories()

    if request.method == 'POST':
        data = {
            'service_name': request.form.get('service_name', ''),
            'category': request.form.get('category', ''),
            'custom_category': request.form.get('custom_category', ''),
            'price': request.form.get('price', ''),
            'description': request.form.get('description', ''),
            'status': request.form.get('status', 'Active')
        }

        if data['category'] == 'NEW' and data['custom_category']:
            data['category'] = data['custom_category']

        updated_service, errors = ServiceService.update_service(service_id, data)
        if errors:
            for err in errors:
                flash(err, 'danger')
            return render_template('services/edit.html', service=target_service, categories=categories, data=data)

        flash(f"Laundry service '{updated_service.service_name}' updated successfully.", "success")
        return redirect(url_for('services.index'))

    return render_template('services/edit.html', service=target_service, categories=categories)


@services_bp.route('/<int:service_id>/toggle-status', methods=['POST'])
@roles_required('Administrator', 'Manager')
def toggle_status(service_id):
    """Toggles status of a laundry service (Active <-> Inactive)."""
    service, message = ServiceService.toggle_service_status(service_id)
    if service:
        flash(message, "success")
    else:
        flash(message, "danger")
    return redirect(request.referrer or url_for('services.index'))


@services_bp.route('/<int:service_id>/delete', methods=['POST'])
@roles_required('Administrator', 'Manager')
def delete(service_id):
    """Performs soft delete on a laundry service."""
    success, message = ServiceService.soft_delete_service(service_id)
    if success:
        flash(message, "success")
    else:
        flash(message, "danger")
    return redirect(url_for('services.index'))


@services_bp.route('/api/active', methods=['GET'])
@login_required
def api_active_services():
    """JSON API returning active non-deleted laundry services for order creation."""
    active_services = ServiceService.get_active_services()
    data = [service.to_dict() for service in active_services]
    return jsonify({'success': True, 'data': data})
