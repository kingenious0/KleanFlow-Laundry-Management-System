"""
Payments Blueprint Routes for KleanFlow Monetary Transactions.
"""

from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.decorators.auth_decorators import roles_required
from app.services_layer.payment_service import PaymentService
from app.services_layer.order_service import OrderService

payments_bp = Blueprint('payments', __name__, url_prefix='/payments')


@payments_bp.route('/', methods=['GET'])
@login_required
def index():
    """Renders payments directory table with search and pagination."""
    search_query = request.args.get('search', '').strip()
    payment_method = request.args.get('payment_method', '').strip()
    order_id = request.args.get('order_id', type=int)
    page = request.args.get('page', 1, type=int)

    pagination = PaymentService.list_payments(
        search_query=search_query,
        payment_method=payment_method,
        order_id=order_id,
        page=page,
        per_page=10
    )

    selected_order = OrderService.get_order_by_id(order_id) if order_id else None

    return render_template(
        'payments/index.html',
        pagination=pagination,
        payments=pagination.items,
        search=search_query,
        selected_method=payment_method,
        selected_order=selected_order
    )


@payments_bp.route('/record', methods=['GET', 'POST'])
@roles_required('Administrator', 'Manager', 'Cashier')
def record():
    """Renders payment recording form and processes payment transaction."""
    preselected_order_id = request.args.get('order_id', type=int)
    preselected_order = OrderService.get_order_by_id(preselected_order_id) if preselected_order_id else None

    if request.method == 'POST':
        data = {
            'order_id': request.form.get('order_id', ''),
            'amount': request.form.get('amount', ''),
            'payment_method': request.form.get('payment_method', 'Cash')
        }

        created_payment, created_receipt, errors = PaymentService.record_payment(
            data, received_by_user_id=current_user.id
        )

        if errors:
            for err in errors:
                flash(err, 'danger')
            target_order = OrderService.get_order_by_id(data.get('order_id')) if data.get('order_id') else preselected_order
            return render_template('payments/record.html', preselected_order=target_order, data=data)

        flash(f"Payment of GH₵ {created_payment.amount:.2f} recorded successfully for Order #{created_payment.order.order_number}!", "success")
        return redirect(url_for('receipts.show', receipt_id=created_receipt.id))

    return render_template('payments/record.html', preselected_order=preselected_order)


@payments_bp.route('/<int:payment_id>', methods=['GET'])
@login_required
def show(payment_id):
    """Renders payment details view."""
    payment = PaymentService.get_payment_by_id(payment_id)
    if not payment:
        flash("Payment transaction record not found.", "danger")
        return redirect(url_for('payments.index'))

    return render_template('payments/show.html', payment=payment)
