from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from .utils.sms import send_sms

class Customer(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10, unique=True)
    phone = models.CharField(max_length=15, blank=True, null=True, help_text="Customer's phone number (e.g., +254712345678)")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Customer"
        verbose_name_plural = "Customers"

class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='orders')
    item = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order of {self.item} by {self.customer.name}"

    class Meta:
        verbose_name = "Order"
        verbose_name_plural = "Orders"

@receiver(post_save, sender=Order)
def send_order_alert(sender, instance, created, **kwargs):
    if created:
        customer_phone = getattr(instance.customer, 'phone', None)
        if not customer_phone:
            print("No phone number available for customer.")
            return

        message = f"New order created! Item: {instance.item}, Amount: {instance.amount}, Time: {instance.time}"
        response = send_sms(customer_phone, message)
        if response:
            print(f"SMS sent successfully: {response}")
        else:
            print("Failed to send SMS.")