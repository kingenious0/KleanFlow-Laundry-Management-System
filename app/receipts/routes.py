"""
Receipts Blueprint Routes for KleanFlow Official Receipts and Printing.
"""

from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from app.services_layer.receipt_service import ReceiptService

receipts_bp = Blueprint('receipts', __name__, url_prefix='/receipts')


@receipts_bp.route('/', methods=['GET'])
@login_required
def index():
    """Renders receipts directory table with search and pagination."""
    search_query = request.args.get('search', '').strip()
    page = request.args.get('page', 1, type=int)

    pagination = ReceiptService.list_receipts(
        search_query=search_query,
        page=page,
        per_page=10
    )

    return render_template(
        'receipts/index.html',
        pagination=pagination,
        receipts=pagination.items,
        search=search_query
    )


@receipts_bp.route('/<int:receipt_id>', methods=['GET'])
@login_required
def show(receipt_id):
    """Renders official printable receipt view per BR-REC-002."""
    receipt_data = ReceiptService.get_receipt_printable_data(receipt_id)
    if not receipt_data:
        flash("Receipt record not found.", "danger")
        return redirect(url_for('receipts.index'))

    return render_template('receipts/show.html', data=receipt_data)


@receipts_bp.route('/<int:receipt_id>/print', methods=['GET'])
@login_required
def print_receipt(receipt_id):
    """Direct thermal/A4 print view template."""
    receipt_data = ReceiptService.get_receipt_printable_data(receipt_id)
    if not receipt_data:
        flash("Receipt record not found.", "danger")
        return redirect(url_for('receipts.index'))

    return render_template('receipts/print.html', data=receipt_data)
