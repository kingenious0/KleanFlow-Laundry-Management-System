"""
CustomerRepository for database access operations on Customer model.
"""

from app.extensions import db
from app.models.customer import Customer


class CustomerRepository:
    """Repository class encapsulating Customer database queries."""

    @staticmethod
    def get_by_id(customer_id, include_deleted=False):
        """Retrieve customer by primary key ID."""
        query = Customer.query.filter_by(id=customer_id)
        if not include_deleted:
            query = query.filter_by(is_deleted=False)
        return query.first()

    @staticmethod
    def get_by_code(customer_code, include_deleted=False):
        """Retrieve customer by customer code (e.g. CUST-0001)."""
        if not customer_code:
            return None
        query = Customer.query.filter(db.func.lower(Customer.customer_code) == customer_code.strip().lower())
        if not include_deleted:
            query = query.filter_by(is_deleted=False)
        return query.first()

    @staticmethod
    def get_by_phone(phone_number, include_deleted=False):
        """Retrieve customer by phone number."""
        if not phone_number:
            return None
        query = Customer.query.filter_by(phone_number=phone_number.strip())
        if not include_deleted:
            query = query.filter_by(is_deleted=False)
        return query.first()

    @staticmethod
    def filter_customers(search_query=None, page=1, per_page=10, include_deleted=False):
        """
        Filter customers with optional search term and pagination.

        Returns:
            Pagination object
        """
        query = Customer.query

        if not include_deleted:
            query = query.filter_by(is_deleted=False)

        if search_query:
            search_pattern = f"%{search_query.strip()}%"
            query = query.filter(
                db.or_(
                    Customer.full_name.ilike(search_pattern),
                    Customer.customer_code.ilike(search_pattern),
                    Customer.phone_number.ilike(search_pattern),
                    Customer.email.ilike(search_pattern),
                    Customer.address.ilike(search_pattern)
                )
            )

        return query.order_by(Customer.created_at.desc()).paginate(
            page=page, per_page=per_page, error_out=False
        )

    @staticmethod
    def search_api(search_query, limit=10):
        """Quick search for auto-complete JSON API."""
        if not search_query:
            return []
        search_pattern = f"%{search_query.strip()}%"
        return Customer.query.filter_by(is_deleted=False).filter(
            db.or_(
                Customer.full_name.ilike(search_pattern),
                Customer.customer_code.ilike(search_pattern),
                Customer.phone_number.ilike(search_pattern)
            )
        ).order_by(Customer.full_name.asc()).limit(limit).all()

    @staticmethod
    def generate_next_code():
        """Generates the next sequential customer code (e.g. CUST-0001)."""
        last_customer = Customer.query.order_by(Customer.id.desc()).first()
        if not last_customer:
            return "CUST-0001"
        next_id = last_customer.id + 1
        return f"CUST-{next_id:04d}"

    @staticmethod
    def create(customer):
        """Add and commit new customer record."""
        db.session.add(customer)
        db.session.commit()
        return customer

    @staticmethod
    def update(customer):
        """Commit updates to an existing customer record."""
        db.session.commit()
        return customer

    @staticmethod
    def soft_delete(customer):
        """Performs soft delete on customer record."""
        customer.is_deleted = True
        db.session.commit()
        return customer
