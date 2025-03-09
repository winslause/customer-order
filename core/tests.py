from django.test import TestCase, Client
from django.urls import reverse
from django.conf import settings
from core.models import Customer, Order
from core.utils.sms import send_sms
from unittest.mock import patch
import logging

# Set up logging for testing
logger = logging.getLogger(__name__)

@patch('core.utils.sms.send_sms')  # Apply patch at class level
class CustomerOrderTestCase(TestCase):
    def setUp(self):
        # Set TESTING flag to disable signals and ensure DEBUG is True
        self.old_testing = getattr(settings, 'TESTING', False)
        settings.TESTING = True
        self.old_debug = settings.DEBUG
        settings.DEBUG = True

        self.client = Client()
        self.customer = Customer.objects.create(name="John Doe", code="JD001", phone="+254712345678")
        self.order = Order.objects.create(customer=self.customer, item="Laptop", amount=1000, time="2025-03-09 14:00:00")

    def test_customer_creation(self, mock_send_sms):
        """Test if a customer is created successfully."""
        customer = Customer.objects.get(name="John Doe")
        self.assertEqual(customer.code, "JD001")
        self.assertEqual(customer.phone, "+254712345678")

    def test_order_creation(self, mock_send_sms):
        """Test if an order is created successfully."""
        order = Order.objects.get(item="Laptop")
        self.assertEqual(order.amount, 1000)
        self.assertEqual(order.customer, self.customer)

    def test_login_and_navigation(self, mock_send_sms):
        """Test OIDC login and navigation to protected views."""
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        response = self.client.get(reverse('customers'))
        self.assertEqual(response.status_code, 302)  # Redirects to login if not authenticated

    def tearDown(self):
        # Clean up after tests
        settings.TESTING = self.old_testing
        settings.DEBUG = self.old_debug
        Customer.objects.all().delete()
        Order.objects.all().delete()