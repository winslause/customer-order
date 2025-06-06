from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from .utils.sms import send_sms
from mptt.models import MPTTModel, TreeForeignKey
import logging
from django.db import transaction

logger = logging.getLogger(__name__)

class Customer(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10, unique=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)

    def __str__(self):
        return self.name

class Category(MPTTModel):
    name = models.CharField(max_length=100)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='orders')
    products = models.ManyToManyField(Product, through='OrderItem')
    time = models.DateTimeField(auto_now_add=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    notification_sent = models.BooleanField(default=False)

    def __str__(self):
        return f"Order by {self.customer.name} at {self.time}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantity} x {item.product.name} in Order {self.order.id}"

@receiver(post_save, sender=Order)
def send_order_notifications(sender, instance, created, **kwargs):
    if created and not instance.notification_sent:
        logger.debug(f"Processing post_save signal for order {instance.id}. Created: {created}")
        customer_phone = instance.customer.phone
        admin_email = settings.ADMIN_EMAIL

        # Ensure items are committed and visible
        with transaction.atomic():
            instance.refresh_from_db()
            items = instance.order_items.all()
            order_details = "\n".join(
                f"{item.quantity} x {item.product.name} - {item.price}" for item in items
            ) or "No items yet"
            message = (
                f"New order created!\nCustomer: {instance.customer.name}\n"
                f"Total Amount: {instance.total_amount}\nTime: {instance.time}\nItems:\n{order_details}"
            )

        logger.debug(f"Order {instance.id} items count: {items.count()}, details: {order_details}")

        if customer_phone:
            try:
                sms_response = send_sms(customer_phone, message)
                logger.info(f"SMS sent to {customer_phone}: {sms_response}")
                print(f"SMS sent successfully: {sms_response}")
            except Exception as e:
                logger.error(f"Failed to send SMS to {customer_phone}: {e}")
                print(f"Failed to send SMS: {e}")

        if admin_email:
            try:
                send_mail(
                    subject=f"New Order #{instance.id} Placed",
                    message=message,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[admin_email],
                    fail_silently=False,
                )
                logger.info(f"Email sent to admin: {admin_email}")
                print(f"Email sent to admin: {admin_email}")
            except Exception as e:
                logger.error(f"Failed to send email to {admin_email}: {e}")
                print(f"Failed to send email: {e}")

        instance.notification_sent = True
        instance.save(update_fields=['notification_sent'])
        logger.debug(f"Order {instance.id} notification_sent set to True")