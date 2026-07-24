"""
Customer Management Blueprint Routes for KleanFlow.
"""

from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required
from app.decorators.auth_decorators import roles_required
from app.services_layer.customer_service import CustomerService

customers_bp = Blueprint('customers', __name__, url_prefix='/customers')


@customers_bp.route('/', methods=['GET'])
@login_required
def index():
    """Renders customer list table with search and pagination."""
    search_query = request.args.get('search', '').strip()
    page = request.args.get('page', 1, type=int)

    pagination = CustomerService.list_customers(
        search_query=search_query,
        page=page,
        per_page=10
    )

    return render_template(
        'customers/index.html',
        pagination=pagination,
        customers=pagination.items,
        search=search_query
    )


@customers_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    """Renders customer registration form and handles new customer creation."""
    if request.method == 'POST':
        data = {
            'full_name': request.form.get('full_name', ''),
            'phone_number': request.form.get('phone_number', ''),
            'email': request.form.get('email', ''),
            'address': request.form.get('address', '')
        }

        created_customer, errors = CustomerService.create_customer(data)
        if errors:
            for err in errors:
                flash(err, 'danger')
            return render_template('customers/create.html', data=data)

        flash(f"Customer '{created_customer.full_name}' registered successfully with code {created_customer.customer_code}.", "success")
        return redirect(url_for('customers.show', customer_id=created_customer.id))

    return render_template('customers/create.html')


@customers_bp.route('/<int:customer_id>', methods=['GET'])
@login_required
def show(customer_id):
    """Renders detailed Customer Profile and activity history."""
    summary = CustomerService.get_customer_profile_summary(customer_id)
    if not summary:
        flash("Customer record not found.", "danger")
        return redirect(url_for('customers.index'))

    return render_template(
        'customers/profile.html',
        customer=summary['customer'],
        total_orders=summary['total_orders'],
        total_spent=summary['total_spent'],
        orders=summary['orders']
    )


@customers_bp.route('/<int:customer_id>/edit', methods=['GET', 'POST'])
@login_required
def edit(customer_id):
    """Renders customer edit form and handles record updates."""
    target_customer = CustomerService.get_customer_by_id(customer_id)
    if not target_customer:
        flash("Customer not found.", "danger")
        return redirect(url_for('customers.index'))

    if request.method == 'POST':
        data = {
            'full_name': request.form.get('full_name', ''),
            'phone_number': request.form.get('phone_number', ''),
            'email': request.form.get('email', ''),
            'address': request.form.get('address', '')
        }

        updated_customer, errors = CustomerService.update_customer(customer_id, data)
        if errors:
            for err in errors:
                flash(err, 'danger')
            return render_template('customers/edit.html', customer=target_customer, data=data)

        flash(f"Customer record for '{updated_customer.full_name}' updated successfully.", "success")
        return redirect(url_for('customers.show', customer_id=updated_customer.id))

    return render_template('customers/edit.html', customer=target_customer)


@customers_bp.route('/<int:customer_id>/delete', methods=['POST'])
@roles_required('Administrator', 'Manager')
def delete(customer_id):
    """Performs soft delete on customer record."""
    success, message = CustomerService.soft_delete_customer(customer_id)
    if success:
        flash(message, "success")
    else:
        flash(message, "danger")
    return redirect(url_for('customers.index'))


@customers_bp.route('/api/search', methods=['GET'])
@login_required
def api_search():
    """JSON API search endpoint for auto-complete search inputs."""
    query = request.args.get('q', '').strip()
    customers = CustomerService.search_api(query, limit=10)
    results = [
        {
            'id': c.id,
            'customer_code': c.customer_code,
            'full_name': c.full_name,
            'phone_number': c.phone_number,
            'address': c.address
        }
        for c in customers
    ]
    return jsonify({'success': True, 'data': results})
