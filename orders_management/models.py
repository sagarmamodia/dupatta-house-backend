from django.db import models
from django.contrib.auth.models import User 

class PaymentMethodChoices(models.TextChoices):
    UPI = "UPI", "UPI"
    COD = "COD", "Cash on Delivery"

class OrderStatusChoices(models.TextChoices):
    COMPELTED = "COMPLETED", "Order Completed"
    PENDING = "PENDING", "Order Pending"

# Create your models here.
class ProductCategory(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    last_updated_at = models.DateTimeField(auto_now=True)

class Products(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(ProductCategory, null=True, blank=True, on_delete=models.SET_NULL)
    stock = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    last_updated_at = models.DateTimeField(auto_now=True)


class ProductImages(models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    url = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    last_updated_at = models.DateTimeField(auto_now=True)

class Orders(models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    payment_method = models.CharField(choices=PaymentMethodChoices.choices)
    quantity = models.IntegerField()
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    delivery_address = models.TextField()
    pin_code = models.CharField(max_length=6)
    status = models.CharField(choices=OrderStatusChoices.choices)
    created_at = models.DateTimeField(auto_now_add=True)
    last_updated_at = models.DateTimeField(auto_now=True)

class ProductDiscountEntries(models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField()
    percentage = models.DecimalField(max_digits=3, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    last_updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=models.Q(percentage__gte=0) & models.Q(percentage__lte=100),
                name='discout_percentage_valid' 
            )
        ]

class CartEntries(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    last_updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.CheckConstraint(
                check = models.Q(quantity__gte=1),
                name='quantity_valid'
            )
        ]


