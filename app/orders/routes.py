"""
Orders Blueprint Routes for KleanFlow Laundry Order Management.
"""

import json
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from app.decorators.auth_decorators import roles_required
from app.services_layer.order_service import OrderService
from app.services_layer.customer_service import CustomerService
from app.services_layer.service_service import ServiceService

orders_bp = Blueprint('orders', __name__, url_prefix='/orders')


@orders_bp.route('/', methods=['GET'])
@login_required
def index():
    """Renders order directory table with search, status tabs, and pagination."""
    search_query = request.args.get('search', '').strip()
    status = request.args.get('status', '').strip()
    payment_status = request.args.get('payment_status', '').strip()
    customer_id = request.args.get('customer_id', type=int)
    page = request.args.get('page', 1, type=int)

    pagination = OrderService.list_orders(
        search_query=search_query,
        status=status,
        payment_status=payment_status,
        customer_id=customer_id,
        page=page,
        per_page=10
    )

    selected_customer = CustomerService.get_customer_by_id(customer_id) if customer_id else None

    return render_template(
        'orders/index.html',
        pagination=pagination,
        orders=pagination.items,
        search=search_query,
        selected_status=status,
        selected_payment_status=payment_status,
        selected_customer=selected_customer
    )


@orders_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    """Renders new order creation form and handles multi-item order placement."""
    active_services = ServiceService.get_active_services()
    preselected_customer_id = request.args.get('customer_id', type=int)
    preselected_customer = CustomerService.get_customer_by_id(preselected_customer_id) if preselected_customer_id else None

    if request.method == 'POST':
        customer_id = request.form.get('customer_id')

        # Parse JSON line items payload from hidden form input or arrays
        items_json = request.form.get('items_json')
        items_data = []

        if items_json:
            try:
                items_data = json.loads(items_json)
            except json.JSONDecodeError:
                items_data = []

        if not items_data:
            # Fallback parsing from form field arrays
            service_ids = request.form.getlist('service_id[]')
            quantities = request.form.getlist('quantity[]')
            clothing_types = request.form.getlist('clothing_type[]')

            for s_id, qty, c_type in zip(service_ids, quantities, clothing_types):
                if s_id and s_id.strip():
                    items_data.append({
                        'service_id': s_id,
                        'quantity': qty,
                        'clothing_type': c_type
                    })

        payload = {
            'customer_id': customer_id,
            'items': items_data
        }

        created_order, errors = OrderService.create_order(payload, created_by_user_id=current_user.id)
        if errors:
            for err in errors:
                flash(err, 'danger')
            return render_template(
                'orders/create.html',
                active_services=active_services,
                preselected_customer=preselected_customer,
                form_data=payload
            )

        flash(f"Order #{created_order.order_number} created successfully!", "success")
        return redirect(url_for('orders.show', order_id=created_order.id))

    return render_template(
        'orders/create.html',
        active_services=active_services,
        preselected_customer=preselected_customer
    )


@orders_bp.route('/<int:order_id>', methods=['GET'])
@login_required
def show(order_id):
    """Renders detailed order information, workflow pipeline, and item breakdown."""
    order = OrderService.get_order_by_id(order_id)
    if not order:
        flash("Order not found.", "danger")
        return redirect(url_for('orders.index'))

    return render_template('orders/show.html', order=order)


@orders_bp.route('/<int:order_id>/status', methods=['POST'])
@login_required
def update_status(order_id):
    """Updates order processing status stage."""
    new_status = request.form.get('order_status', '').strip()
    order, messages = OrderService.update_order_status(order_id, new_status)

    if order:
        flash(messages[0], "success")
    else:
        for msg in messages:
            flash(msg, "danger")

    return redirect(url_for('orders.show', order_id=order_id))


@orders_bp.route('/<int:order_id>/cancel', methods=['POST'])
@roles_required('Administrator', 'Manager', 'Cashier')
def cancel(order_id):
    """Cancels an order per BR-ORD-004."""
    success, message = OrderService.cancel_order(order_id)
    if success:
        flash(message, "success")
    else:
        flash(message, "danger")
    return redirect(url_for('orders.show', order_id=order_id))
