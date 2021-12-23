from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import serializers

from accounts.models import Account
from store.models import Product
from .models import Cart, Cartitem, ItemVariation
from .serializers import CartSerializer, CartItemSerializer
from utils.carts import get_cart_id


class CartList(APIView):

    def get(self, request):
        cart_item = None
        if request.user.is_authenticated:
            cart_item = Cartitem.objects.filter(user=request.user).order_by('product')
        else:
            cart_id = get_cart_id(request)
            try:
                cart = Cart.objects.get(cart_id=cart_id)
                cart_item = Cartitem.objects.filter(
                    cart=cart).order_by('product')
            except Cart.DoesNotExist:
                cart_item = None
                
            
        serializer = CartItemSerializer(cart_item, many=True)
        
        return Response(serializer.data)


class AddToCart(APIView):
    
    def post(self, request):
        serializer = CartSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            data = serializer.validated_data
            
            product_id = data['product_id']
            color = data['color']
            size = data['size']
            brand = data['brand']
            quantity = data['quantity']
          
            
            # create a variation id
            variation_id = f'{product_id}{color}{size}{brand}'

            # check  if product id is currect
            try:
                product = Product.objects.get(pk=product_id)
            except Product.DoesNotExist:
                raise serializers.ValidationError(
                    {'product': 'product not found!'})

            # get cart or create one if none exists
            cart_id = get_cart_id(request)
            try:
                cart = Cart.objects.get(cart_id=cart_id)
            except Cart.DoesNotExist:
                cart = Cart.objects.create(cart_id=cart_id)
                cart.save()
                
            # if user is logged in
            if request.user.is_authenticated:
                user = Account.objects.get(pk=request.user.id)
                existing_item = Cartitem.objects.filter(
                    product=product, variation__variation_id=variation_id, user=user).exists()
                if existing_item:
                    cart_item = Cartitem.objects.get(
                        product=product, variation__variation_id=variation_id, user=user)
                    cart_item.quantity += quantity
                    cart_item.save()
                else:
                    variarion = ItemVariation.objects.create(
                        variation_id=variation_id,
                        color=color,
                        size=size,
                        brand=brand
                    )
                    # variarion.save()
                    cart_item = Cartitem()
                    cart_item.user = user
                    cart_item.cart = cart
                    cart_item.product = product
                    cart_item.variation = variarion
                    cart_item.quantity = quantity
                    cart_item.save()
            # if not logged in
            else:  
                # check if cart item already exist
                existing_item = Cartitem.objects.filter(product=product, variation__variation_id=variation_id, cart=cart).exists()
                
                if existing_item:
                    cart_item = Cartitem.objects.get(product=product, variation__variation_id=variation_id)
                    cart_item.quantity += quantity
                    cart_item.save()
                else:
                    variarion = ItemVariation.objects.create(
                        variation_id=variation_id,
                        color=color,
                        size=size,
                        brand=brand
                    )
                    # variarion.save()
                    cart_item = Cartitem()
                    cart_item.cart = cart
                    cart_item.product = product
                    cart_item.variation = variarion
                    cart_item.quantity = quantity
                    cart_item.save()
             
                return Response({'success': cart_item.product.product_name + 'added to cart'})
        return Response()


class IncrementCartItem(APIView):
    
    def post(self, request):
        item_id = request.data.get('item_id')
        cart_item = Cartitem.objects.get(id=item_id)
        cart_item.quantity += 1
        cart_item.save()       
        return Response()
    
    
class DecrementCartItem(APIView):
    
    def post(self, request):
        item_id = request.data.get('item_id')
        cart_item = Cartitem.objects.get(id=item_id)
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()       
        else:
            cart_item.delete()
        return Response()
    
    
class RemoveCartItem(APIView):
    
    def post(self, request):
        item_id = request.data.get('item_id')
        cart_item = Cartitem.objects.get(id=item_id)
        cart_item.delete()
        
        return Response()
