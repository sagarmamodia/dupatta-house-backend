from django.db import models
from django.contrib.auth.models import User 

# Create your models here.
class ProductCategory(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    last_updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(ProductCategory, null=True, blank=True, on_delete=models.SET_NULL)
    stock = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    last_updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    file_id = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    last_updated_at = models.DateTimeField(auto_now=True)

class Order(models.Model):
   
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('shipped', 'Shipped'),
        ('cancelled', 'Cancelled'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    delivery_address = models.TextField()
    pincode = models.CharField(max_length=6)
    contact_number = models.CharField(max_length=13)
    status = models.CharField(choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    last_updated_at = models.DateTimeField(auto_now=True)

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField(default=1)
    price_per_unit = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    # discount = models.ForeignKey(ProductDiscountEntry, on_delete=models.PROTECT, null=True, blank=True)
    
    def save(self, *args, **kwargs):
        if self.price_per_unit is None:
            self.price_per_unit = self.product.price

        if self.subtotal is None:
            self.subtotal = self.quantity * self.price_per_unit 

        super().save(*args, **kwargs)


class Payment(models.Model):
    STATUS_CHOICES = [
        ('created', 'Created'),
        ('paid', 'Paid'),
        ('failed', 'Failed'),
    ]

    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name = 'payment')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='payments')
    razorpay_order_id = models.CharField(max_length=100, unique=True)
    amount = models.PositiveIntegerField(
         help_text="Amount in paise (e.g. ₹1 = 100 paise), because Razorpay expects paise"
    )
    currency = models.CharField(max_length=10, default='NULL')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='created')
    created_at = models.DateTimeField(auto_now_add=True)
    last_updated_at = models.DateTimeField(auto_now=True)

class CartEntry(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
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

# class ProductDiscountEntry(models.Model):
#     STATUS_CHOICES = [
#         ('active', 'Active'),
#         ('discontinued', 'Discontinued')
#     ]
#     product = models.ForeignKey(Product, on_delete=models.CASCADE)
#     name = models.CharField(max_length=100)
#     description = models.TextField()
#     percentage = models.DecimalField(max_digits=3, decimal_places=2)
#     created_at = models.DateTimeField(auto_now_add=True)
#     status = models.CharField(choices=STATUS_CHOICES, default='active')
#     last_updated_at = models.DateTimeField(auto_now=True)
#
#     class Meta:
#         constraints = [
#             models.CheckConstraint(
#                 check=models.Q(percentage__gte=0) & models.Q(percentage__lte=100),
#                 name='discout_percentage_valid' 
#             )
#         ]
#
