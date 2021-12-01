from django.http import request
from django.shortcuts import render

from rest_framework.response import Response
from rest_framework.views import APIView


from .serializers import ProductSerializer, ReviewSerialzer
from .models import Product


class ProductList(APIView):
    
    def get(self, request):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)


class ProductDetail(APIView):
    
    def get(self, request, slug):
        product = Product.objects.get(slug=slug)
        serializer = ProductSerializer(product)
        return Response(serializer.data)


class AddReview(APIView):
    
    def post(self, request):
        serializer = ReviewSerialzer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        
        return Response({'created': True})
