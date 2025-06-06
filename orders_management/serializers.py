from rest_framework import serializers
from .models import Product, ProductCategory, ProductImage, Order, CartEntry, OrderItem, Payment
from django.contrib.auth.models import User

class ProductSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        queryset=ProductCategory.objects.all(),
        slug_field='name'
    )

    class Meta:
        model = Product
        fields = '__all__'

class CartEntrySerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    product = serializers.SlugRelatedField(
        queryset=Product.objects.all(),
        slug_field='id'
    )

    class Meta:
        model = CartEntry
        fields = '__all__'

        read_only_fields = ['user']

    def get_user(self, obj):
        return obj.user.username

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = '__all__'
        read_only_fields = ["user", "order", "price_per_unit", "subtotal", "created_at", "last_updated_at"]

class OrderWithOrderItemsSerializer(serializers.ModelSerializer):    
    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = '__all__'
        read_only_fields = ["user", "created_at", "updated_at"]
        
    def create(self, validated_data, *args, **kwargs):
        items = validated_data.pop("items", None)
        order = Order.objects.create(**validated_data)
        print(order)
        for item in items:
            OrderItem.objects.create(order=order, **item)

        return order
                
class PaymentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Payment 
        fields = '__all__'
        read_only_fields = ["user", "amount"]
            
    




