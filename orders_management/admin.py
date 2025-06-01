from django.contrib import admin
from . import models

# Register your models here.
admin.site.register(models.Products)
admin.site.register(models.ProductCategory)
admin.site.register(models.ProductDiscountEntries)
admin.site.register(models.ProductImages)
admin.site.register(models.CartEntries)
admin.site.register(models.Orders)
