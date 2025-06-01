from rest_framework import serializers
from .models import Products, ProductCategory, ProductImages, Orders, ProductDiscountEntries, CartEntries
from django.contrib.auth.models import User

class ProductsSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        queryset=ProductCategory.objects.all(),
        slug_field='name'
    )

    class Meta:
        model = Products 
        fields = '__all__'


class ProductCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCategory

class ProductImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImages

class OrdersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Orders
        fields = '__all__'

class ProductDiscountEntriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductDiscountEntries

class CartEntriesSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    product = serializers.SlugRelatedField(
        queryset=Products.objects.all(),
        slug_field='id'
    )

    class Meta:
        model = CartEntries
        fields = '__all__'

        read_only_fields = ['user']

    def get_user(self, obj):
        return obj.user.username

