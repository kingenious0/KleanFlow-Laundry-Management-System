"""
CustomerService handling business logic for Customer Management.
"""

from app.models.customer import Customer
from app.repositories.customer_repository import CustomerRepository
from app.validators.customer_validator import CustomerValidator


class CustomerService:
    """Service layer class for customer administration."""

    @staticmethod
    def get_customer_by_id(customer_id, include_deleted=False):
        """Retrieve customer by ID."""
        return CustomerRepository.get_by_id(customer_id, include_deleted=include_deleted)

    @staticmethod
    def list_customers(search_query=None, page=1, per_page=10):
        """Retrieve paginated active customer list with optional search query."""
        return CustomerRepository.filter_customers(
            search_query=search_query,
            page=page,
            per_page=per_page
        )

    @staticmethod
    def create_customer(data):
        """
        Registers a new customer after validation.

        Returns:
            tuple: (created Customer or None, list of error messages)
        """
        errors = CustomerValidator.validate_customer_creation(data)
        if errors:
            return None, errors

        customer_code = data.get('customer_code', '').strip()
        if not customer_code:
            customer_code = CustomerRepository.generate_next_code()

        customer = Customer(
            customer_code=customer_code,
            full_name=data.get('full_name', '').strip(),
            phone_number=data.get('phone_number', '').strip(),
            email=data.get('email', '').strip() if data.get('email') else None,
            address=data.get('address', '').strip(),
            is_deleted=False
        )

        created_customer = CustomerRepository.create(customer)
        return created_customer, []

    @staticmethod
    def update_customer(customer_id, data):
        """
        Updates an existing customer record.

        Returns:
            tuple: (updated Customer or None, list of error messages)
        """
        customer = CustomerRepository.get_by_id(customer_id)
        if not customer:
            return None, ["Customer not found."]

        errors = CustomerValidator.validate_customer_update(customer_id, data)
        if errors:
            return None, errors

        customer.full_name = data.get('full_name', customer.full_name).strip()
        customer.phone_number = data.get('phone_number', customer.phone_number).strip()
        customer.email = data.get('email', '').strip() if data.get('email') else None
        customer.address = data.get('address', customer.address).strip()

        updated_customer = CustomerRepository.update(customer)
        return updated_customer, []

    @staticmethod
    def soft_delete_customer(customer_id):
        """
        Soft deletes a customer record while retaining history per BR-CUS-003.

        Returns:
            tuple: (success boolean, message string)
        """
        customer = CustomerRepository.get_by_id(customer_id)
        if not customer:
            return False, "Customer not found."

        CustomerRepository.soft_delete(customer)
        return True, f"Customer '{customer.full_name}' successfully removed."

    @staticmethod
    def get_customer_profile_summary(customer_id):
        """
        Calculates and returns summary statistics for customer profile dashboard.

        Returns:
            dict: profile metrics & orders summary
        """
        customer = CustomerRepository.get_by_id(customer_id)
        if not customer:
            return None

        total_orders = len(customer.orders) if customer.orders else 0
        total_spent = sum([order.total_amount for order in customer.orders if hasattr(order, 'total_amount') and order.total_amount]) if customer.orders else 0.0

        return {
            'customer': customer,
            'total_orders': total_orders,
            'total_spent': total_spent,
            'orders': customer.orders or []
        }

    @staticmethod
    def search_api(query, limit=10):
        """Returns customer list for JSON auto-complete API."""
        return CustomerRepository.search_api(query, limit=limit)
