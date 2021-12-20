from django.db.models import Sum
from django.shortcuts import render

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import permissions

from orders.models import OrderProduct
from .serializers import ProductSerializer, ReviewSerialzer, TopProductSerializer, CategorySerializer
from .models import Category, Product, Review


class ProductList(APIView):

    def get(self, request):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)
    
    
class TopProducts(APIView):
    '''this get the top selling products from the store'''

    def get(self, request):
        #* values() group by product_id
        #* annotate() calculate the total of each product sales
        #* value_list() return id of each the product, flat=True makes sure to return list of id instead of list of id tuples
        top_products = OrderProduct.objects.values('product_id').annotate(
            total=Sum('quantity')).order_by('-total')[:3].values_list('product_id', flat=True)
        products = Product.objects.filter(pk__in=top_products)
        serializer = TopProductSerializer(products, many=True)
        return Response(serializer.data)


class ProductDetail(APIView):

    def get(self, request, slug):
        user = request.user
        is_purchased = False
        already_reviewed = False
        product = Product.objects.get(slug=slug)
        if user.is_authenticated:
            is_purchased = OrderProduct.objects.filter(
                product__slug=slug, user=user).exists()
            # check if user already submitted a review for this product
            already_reviewed = Review.objects.filter(product=product, user=user).exists() 
        serializer = ProductSerializer(product)
        return Response({'product': serializer.data, 'is_purchased': is_purchased, 'already_reviewed': already_reviewed})


class AddReview(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = ReviewSerialzer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            data = serializer.data
            current_user = request.user
            product = Product.objects.get(pk=data['product'])

            review = Review()
            review.user = current_user
            review.product = product
            review.subject = data['subject']
            review.review = data['review']
            review.rating = data['rating']
            review.save()

        return Response({'created': True})
    
class UpdateReview(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def put(self, request, pk):
        review = Review.objects.get(id=pk)
        serializer = ReviewSerialzer(review, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()

            return Response({'updated': True})
        else:
            return Response(serializer.errors)


class DeleteReview(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def delete(self,request, pk):
        data = None
        try:
            review = Review.objects.get(id=pk)
            review.delete()
            data = {'deleted': True}
        except Review.DoesNotExist:
           data = {'deleted': False}
        
        return Response(data)
        

class CategoryListView(APIView):
    
    def get(self, request):
        # filter categories with image
        categories = Category.objects.exclude(image__isnull=True).exclude(image__exact='') 
        serializer = CategorySerializer(categories, many=True)    
        return Response(serializer.data)