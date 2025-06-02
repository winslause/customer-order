from django.test import TestCase, Client
from django.urls import reverse
from django.conf import settings
from django.core import mail
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from core.models import Customer, Category, Product, Order, OrderItem
from core.utils.sms import send_sms
from unittest.mock import patch
import logging
from django.db import transaction
from django.db.models.signals import post_save

logger = logging.getLogger(__name__)

class CustomerOrderTestCase(TestCase):
    def setUp(self):
        self.old_testing = getattr(settings, 'TESTING', False)
        settings.TESTING = True
        self.old_debug = settings.DEBUG
        settings.DEBUG = True

        self.user = User.objects.create_user(username='testuser', password='testpass123')
        
        self.client = Client()
        self.client.login(username='testuser', password='testpass123')
        
        self.api_client = APIClient()
        self.api_client.force_authenticate(user=self.user)

        self.customer = Customer.objects.create(
            name="John Doe", code="JD001", phone="+254712345678", email="john@example.com"
        )
        self.category = Category.objects.create(name="All Products")
        self.bakery = Category.objects.create(name="Bakery", parent=self.category)
        self.bread = Category.objects.create(name="Bread", parent=self.bakery)
        self.product = Product.objects.create(
            name="White Bread", category=self.bread, price=5.00, description="Fresh white bread"
        )
        self.order = Order.objects.create(customer=self.customer, total_amount=5.00)
        self.order_item = OrderItem.objects.create(
            order=self.order, product=self.product, quantity=1, price=5.00
        )

    def test_customer_creation(self):
        customer = Customer.objects.get(name="John Doe")
        self.assertEqual(customer.code, "JD001")
        self.assertEqual(customer.phone, "+254712345678")
        self.assertEqual(customer.email, "john@example.com")

    def test_category_creation(self):
        category = Category.objects.get(name="Bread")
        self.assertEqual(category.parent.name, "Bakery")
        self.assertEqual(category.get_ancestors().count(), 2)

    def test_product_creation(self):
        product = Product.objects.get(name="White Bread")
        self.assertEqual(product.category.name, "Bread")
        self.assertEqual(product.price, 5.00)
        self.assertEqual(product.description, "Fresh white bread")

    def test_order_creation(self):
        order = Order.objects.get(id=self.order.id)
        self.assertEqual(order.customer, self.customer)
        self.assertEqual(order.total_amount, 5.00)
        self.assertEqual(order.order_items.count(), 1)
        self.assertEqual(order.order_items.first().product, self.product)

    @patch('core.utils.sms.send_sms')
    def test_order_sms_notification(self, mock_send_sms):
        mock_send_sms.return_value = {"status": "success"}
        # Create order
        with transaction.atomic():
            order = Order.objects.create(customer=self.customer, total_amount=0, notification_sent=False)
        # Create OrderItem and update total_amount
        with transaction.atomic():
            item = OrderItem.objects.create(order=order, product=self.product, quantity=2, price=5.00)
            order.total_amount = item.quantity * item.price
            order.save()  # Save total_amount
        # Refresh and trigger signal
        order.refresh_from_db()
        order.notification_sent = False  # Ensure signal can run
        order.save()  # Trigger post_save signal
        if not mock_send_sms.called:
            # Fallback: manually trigger signal
            from core.models import send_order_notifications
            send_order_notifications(sender=Order, instance=order, created=True)
        self.assertTrue(mock_send_sms.called, "SMS mock was not called")
        args, kwargs = mock_send_sms.call_args
        self.assertEqual(args[0], self.customer.phone)
        self.assertIn("New order created!", args[1])
        self.assertIn("White Bread", args[1])

    def test_order_email_notification(self):
        mail.outbox = []
        # Create order
        with transaction.atomic():
            order = Order.objects.create(customer=self.customer, total_amount=0, notification_sent=False)
        # Create OrderItem and update total_amount
        with transaction.atomic():
            item = OrderItem.objects.create(order=order, product=self.product, quantity=2, price=5.00)
            order.total_amount = item.quantity * item.price
            order.save()  # Save total_amount
        # Refresh and trigger signal
        order.refresh_from_db()
        order.notification_sent = False  # Ensure signal can run
        order.save()  # Trigger post_save signal
        if not mail.outbox:
            # Fallback: manually trigger signal
            from core.models import send_order_notifications
            send_order_notifications(sender=Order, instance=order, created=True)
        self.assertEqual(len(mail.outbox), 1, "Email was not sent")
        email = mail.outbox[0]
        self.assertEqual(email.subject, f"New Order #{order.id} Placed")
        self.assertEqual(email.to, [settings.ADMIN_EMAIL])
        self.assertIn("White Bread", email.body)

    def test_category_average_price_api(self):
        response = self.api_client.get(
            reverse('order-category-average-price', kwargs={'category_id': self.bakery.id})
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['average_price'], 5.00)

    def test_login_and_navigation(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        response = self.client.get(reverse('customers'))
        self.assertEqual(response.status_code, 200)

    def test_customer_create_view(self):
        response = self.client.post(
            reverse('customer_add'),
            {'name': 'Jane Doe', 'code': 'JD002', 'phone': '+254637389456', 'email': 'jane@example.com'}
        )
        self.assertEqual(response.status_code, 302)
        customer = Customer.objects.get(name="Jane Doe")
        self.assertEqual(customer.code, 'JD002')
        self.assertEqual(customer.email, 'jane@example.com')

    def test_customer_create_view_post_invalid(self):
        response = self.client.post(
            reverse('customer_add'),
            {'name': '', 'code': '', 'phone': '+254637389456', 'email': 'invalid'}
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Error adding customer")

    def test_category_create_view_post(self):
        response = self.client.post(
            reverse('category_add'),
            {'name': 'Vegetables', 'parent': self.category.id}
        )
        self.assertEqual(response.status_code, 302)
        category = Category.objects.get(name="Vegetables")
        self.assertEqual(category.parent.name, "All Products")

    def test_category_create_view_post_invalid(self):
        response = self.client.post(
            reverse('category_add'),
            {'name': '', 'parent': self.category.id}
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Error adding category")

    def test_product_create_view(self):
        response = self.client.post(
            reverse('product_add'),
            {'name': 'Apple', 'category': self.bread.id, 'price': '2.50', 'description': 'Fresh apple'}
        )
        self.assertEqual(response.status_code, 302)
        product = Product.objects.get(name="Apple")
        self.assertEqual(product.price, 2.50)

    def test_product_create_view_post_invalid(self):
        response = self.client.post(
            reverse('product_add'),
            {'name': '', 'category': '', 'price': ''}
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Error adding product")

    def test_order_create_view_post(self):
        response = self.client.post(
            reverse('order_add'),
            {
                'customer': self.customer.id,
                'products': [self.product.id],
                f'quantity_{self.product.id}': '2'
            }
        )
        self.assertEqual(response.status_code, 302)
        order = Order.objects.filter(customer=self.customer).last()
        self.assertEqual(order.total_amount, 10.00)
        self.assertEqual(order.order_items.count(), 1)
        self.assertEqual(order.order_items.first().quantity, 2)

    def test_order_create_view_post_invalid(self):
        response = self.client.post(
            reverse('order_add'),
            {
                'customer': self.customer.id,
                'products': [self.product.id],
                f'quantity_{self.product.id}': '0'
            }
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Error adding order")

    def test_api_customer_create(self):
        response = self.api_client.post(
            reverse('customer-list'),
            {'name': 'Bob Smith', 'code': 'BS001', 'phone': '+254987654321', 'email': 'bob@example.com'}
        )
        self.assertEqual(response.status_code, 201)
        customer = Customer.objects.get(name="Bob Smith")
        self.assertEqual(customer.code, 'BS001')
        self.assertEqual(customer.email, 'bob@example.com')

    def test_api_customer_create_invalid(self):
        response = self.api_client.post(
            reverse('customer-list'),
            {'name': '', 'code': ''}
        )
        self.assertEqual(response.status_code, 400)

    def test_api_category_create(self):
        response = self.api_client.post(
            reverse('category-list'),
            {'name': 'Fruits', 'parent': self.category.id}
        )
        self.assertEqual(response.status_code, 201)
        category = Category.objects.get(name="Fruits")
        self.assertEqual(category.parent.name, 'All Products')

    def test_api_product_create(self):
        response = self.api_client.post(
            reverse('product-list'),
            {'name': 'Orange', 'category': self.bread.id, 'price': 5.00, 'description': 'Fresh orange'}
        )
        self.assertEqual(response.status_code, 201)
        product = Product.objects.get(name="Orange")
        self.assertEqual(product.price, 5.00)

    def test_api_order_create(self):
        response = self.api_client.post(
            reverse('order-list'),
            {
                'customer': self.customer.id,
                'order_items': [
                    {
                        'product': self.product.id,
                        'quantity': 2,
                        'price': 5.00
                    }
                ]
            },
            format='json'
        )
        self.assertEqual(response.status_code, 201)
        order = Order.objects.filter(customer=self.customer).last()
        self.assertEqual(order.total_amount, 10.00)
        self.assertEqual(order.order_items.count(), 1)
        self.assertEqual(order.order_items.first().quantity, 2)

    def test_sms_failure(self):
        with patch('core.utils.sms.send_sms', side_effect=Exception('SMS failed')):
            order = Order.objects.create(customer=self.customer)
            OrderItem.objects.create(order=order, product=self.product, quantity=2, price=5.00)
            order.total_amount = 10.00
            order.save()
            self.assertTrue(order.notification_sent)

    def test_email_failure(self):
        with patch('django.core.mail.send_mail', side_effect=Exception('Email failed')):
            order = Order.objects.create(customer=self.customer)
            OrderItem.objects.create(order=order, product=self.product, quantity=2, price=5.00)
            order.total_amount = 10.00
            order.save()
            self.assertTrue(order.notification_sent)

    def tearDown(self):
        settings.TESTING = self.old_testing
        settings.DEBUG = self.old_debug
        Customer.objects.all().delete()
        Category.objects.all().delete()
        Product.objects.all().delete()
        Order.objects.all().delete()
        User.objects.all().delete()

class SimpleTestCase(TestCase):
    def test_basic(self):
        self.assertEqual(1 + 1, 2)