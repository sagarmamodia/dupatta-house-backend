from django.shortcuts import render
from rest_framework import generics, status 
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from .models import Products, CartEntries, Orders
from .serializers import ProductsSerializer, CartEntriesSerializer, OrdersSerializer
from .mongodb import fs

# class AddProductView(generics.CreateAPIView):
#     queryset = Products.objects.all()
#     serializer_class = ProductsSerializer
#
# class UpdateProductView(generics.UpdateAPIView):
#     queryset = Products.objects.all() 
#     serializer_class = ProductsSerializer 
#     lookup_field='id'

class ListProductView(generics.ListAPIView):
    queryset = Products.objects.all()
    serializer_class = ProductsSerializer

class AddCartEntryView(generics.CreateAPIView):
    queryset = CartEntries.objects.all()
    serializer_class = CartEntriesSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class ListCartEntriesView(generics.ListAPIView):
    queryset = CartEntries.objects.all()
    serializer_class = CartEntriesSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return CartEntries.objects.filter(user=self.request.user)

class AddCreateOrderView(generics.CreateAPIView):
    queryset = Orders.objects.all()
    serializer_class = OrdersSerializer
    permission_classes = [IsAuthenticated]

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
