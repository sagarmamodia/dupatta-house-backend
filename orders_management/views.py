from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest
from django.db import transaction
from django.conf import settings
from rest_framework import generics, status 
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.parsers import MultiPartParser, FormParser
from .models import Product, CartEntry, Order, OrderItem, Payment
from .serializers import ProductSerializer, CartEntrySerializer, OrderWithOrderItemsSerializer, PaymentSerializer
from .mongodb import fs
import random
import hmac 
import hashlib

# class AddProductView(generics.CreateAPIView):
#     queryset = Products.objects.all()
#     serializer_class = ProductsSerializer
#
# class UpdateProductView(generics.UpdateAPIView):
#     queryset = Products.objects.all() 
#     serializer_class = ProductsSerializer 
#     lookup_field='id'

class ListProductView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class AddCartEntryView(generics.CreateAPIView): 
    queryset = CartEntry.objects.all()
    serializer_class = CartEntrySerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class ListCartEntriesView(generics.ListAPIView):
    queryset = CartEntry.objects.all()
    serializer_class = CartEntrySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return CartEntry.objects.filter(user=self.request.user)

class CreateOrderView(generics.CreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderWithOrderItemsSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class ListUserOrdersView(generics.ListAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderWithOrderItemsSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

class InitiatePaymentView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):

        order_id = request.data.get('order', None)
        if order_id is None:
            return Response({"error": "order is required in POST data."}, status=status.HTTP_400_BAD_REQUEST)

        order_items = OrderItem.objects.filter(order__id=order_id) 
        amount = 0 
        for item in order_items:
            amount += item.subtotal
        amount_paise = amount*100

        try:
            client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
            razorpay_order = client.order.create({
                "amount": amount_paise,
                "currency": "INR",
                "payment_capture": 1
            })
        except:
            # return Response({"error": "Failed to create razorpay order please try again."}, status=500)
            razorpay_order_id = f"razorpay_id_{order_id}_{random.random()}"

        payment_data = request.data
        payment_data['razorpay_order_id'] = razorpay_order_id
        payment_data['amount'] = amount_paise
        payment_data['currency'] = "INR"
        serializer = PaymentSerializer(data=payment_data) 
        if serializer.is_valid(raise_exception=True):    
            serializer.save(amount=amount_paise, user=request.user)
        else:
            return Response({"error": "Failure to create payment in database"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

        return Response({
            "order_id": razorpay_order_id,
            "razorpay_key": settings.RAZORPAY_KEY_ID,
            "amount": amount_paise, 
            "currency": "INR"
        }, status=status.HTTP_201_CREATED)

        
class RazorpayCallbackView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        razorpay_order_id = request.data.get('razorpay_order_id') 
        razorpay_payment_id = request.data.get('razorpay_payment_id')
        payment_signature = request.data.get('razorpay_signature')

        try:
            payment_obj = Payment.objects.get(razorpay_order_id=razorpay_order_id)
        except:
            return Response({"error": f"Payment with {razorpay_order_id} does not exist"}, status=HTTP_400_BAD_REQUEST)
        if razorpay_payment_id is None:
            payment_obj.delete()
            return Response({"error": "Payment failed and deleted from database"}, status=HTTP_400_BAD_REQUEST)
        
        #signature verification
        body = f"{razorpay_order_id}|{razorpay_payment_id}"
        generated_signature = hmac.new(
            settings.RAZORPAY_KEY_SECRET.encode(),
            body.encode(),
            hashlib.sha256
        ).hexdigest()

        if hmac.compare_digest(generated_signature, payment_signature):
            payment_obj.status = 'paid'
            payment_obj.order.status = 'paid'
            payment_obj.order.save()
            payment_obj.save()
        
        return Response({
            "message": "Payment done"
        }, status=200)


# class ImageUploadView(APIView):
#     parser_classes = [MultiPartParser, FormParser]
#     permission_classes = [IsAuthenticated]
#
#     def post(self, request):
#         file = request.Files.get('file')
#
#         if not file:
#             return Response({"error": "No file provided"}, status=status.HTTP_400_BAD_REQUEST)
#
#         file_id = fs.put(file, filename=file.name, content_type=file.content_type)
#
#
#         return Response({
#             "message": "File uploaded successfully",
#             "file_id": str(file_id)
#             }, status=status.HTTP_201_CREATED)
