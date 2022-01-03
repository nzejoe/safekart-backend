from django.shortcuts import render
from django.db.models import Sum

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import permissions

from carts.models import Cartitem
from .serializers import (OrderHistorySerializer, OrderSerializer,
                          OrderDetailSerializer, TopProductSerializer, OrderProductSerializer)
from .models import Payment, OrderDetail, OrderProduct


class PlaceOrder(APIView):
    permission_classes = [permissions.IsAuthenticated, ]

    def post(self, request, data=None):
        serializer = OrderSerializer(
            data=request.data, context={'request': request})

        if serializer.is_valid(raise_exception=True):
            current_user = request.user
            cart_items = Cartitem.objects.filter(user=current_user)

            data = serializer.validated_data

            # payment
            payment_id = data['payment_id']
            grand_total = data['grand_total']
            payment_method = data['payment_method']
            payment_status = data['payment_status']

            # order
            order_number = data['order_number']
            total_amount = data['total_amount']
            tax = data['tax']
            first_name = data['first_name']
            middle_name = data['middle_name']
            last_name = data['last_name']
            gender = data['gender']
            email = data['email']
            phone = data['phone']
            address_1 = data['address_1']
            address_2 = data['address_2']
            city = data['city']
            state = data['state']
            country = data['country']

            # create payment
            payment = Payment()
            payment.payment_id = payment_id
            payment.user = current_user
            payment.amount = grand_total
            payment.payment_method = payment_method
            payment.status = payment_status
            payment.save()

            # create order
            order = OrderDetail()
            order.order_number = order_number
            order.payment = payment
            order.user = current_user
            order.first_name = first_name
            order.middle_name = middle_name
            order.last_name = last_name
            order.gender = gender
            order.email = email
            order.phone = phone
            order.address_1 = address_1
            order.address_2 = address_2
            order.city = city
            order.state = state
            order.country = country
            order.total_amount = total_amount
            order.tax = tax
            order.grand_total = grand_total
            order.is_ordered = True
            order.save()

            # order products
            for item in cart_items:
                product = OrderProduct()
                product.order = order
                product.product = item.product
                product.user = current_user
                product.color = item.variation.color
                product.size = item.variation.size
                product.brand = item.variation.brand
                product.price = item.product.price
                product.quantity = item.quantity
                product.save()

                # delete cart_item after
                item.delete()

        return Response(data)


class UserOrderHistory(APIView):
    permission_classes = [permissions.IsAuthenticated, ]

    def get(self, request):
        my_orders = OrderDetail.objects.filter(
            user=request.user).order_by('-created')
        serializer = OrderHistorySerializer(my_orders, many=True)
        return Response(serializer.data)


class OrderDetailView(APIView):
    permission_classes = [permissions.IsAuthenticated, ]

    def get(self, request, order_number):
        order = OrderDetail.objects.get(
            user=request.user, order_number=order_number)
        serializer = OrderDetailSerializer(order)
        return Response(serializer.data)


class OrderHistory(APIView):
    permission_classes = [permissions.AllowAny, ]

    def get(self, request):
        orders = OrderProduct.objects.all().order_by('-created')
        serializer = OrderProductSerializer(orders, many=True)
        return Response(serializer.data)


class TopSelling(APIView):
    permission_classes = [permissions.AllowAny, ]

    def get(self, request):
        top = OrderProduct.objects.values('product_name').annotate(
            total=Sum('quantity')).order_by('-total')[:5]

        serializer = TopProductSerializer(top, many=True)

        return Response(serializer.data)
