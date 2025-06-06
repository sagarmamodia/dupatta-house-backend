from django.contrib import admin
from . import models

# Register your models here.
admin.site.register(models.Product)
admin.site.register(models.ProductCategory)
admin.site.register(models.ProductImage)
admin.site.register(models.CartEntry)
admin.site.register(models.Order)
admin.site.register(models.Payment)
admin.site.register(models.OrderItem)
# admin.site.register(models.ProductDiscountEntry)
