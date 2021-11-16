from django.shortcuts import render

from rest_framework.response import Response
from rest_framework.views import APIView


from .serializers import ProductSerializer
from .models import Product


class ProductList(APIView):
    
    def get(self, request):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)