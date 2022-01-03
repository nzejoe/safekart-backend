from django.db.models import fields
from rest_framework import serializers

from .models import OrderDetail, OrderProduct


class OrderSerializer(serializers.Serializer):
    payment_id = serializers.CharField()
    grand_total = serializers.DecimalField(decimal_places=2, max_digits=20)
    payment_status = serializers.CharField()
    payment_method = serializers.CharField()
    order_number = serializers.CharField()
    total_amount = serializers.DecimalField(decimal_places=2, max_digits=20)
    tax = serializers.DecimalField(decimal_places=2, max_digits=20)
    first_name = serializers.CharField()
    middle_name = serializers.CharField(allow_null=True, allow_blank=True)
    last_name = serializers.CharField()
    gender = serializers.CharField()
    email = serializers.EmailField()
    phone = serializers.CharField()
    address_1 = serializers.CharField()
    address_2 = serializers.CharField(allow_null=True, allow_blank=True)
    city = serializers.CharField()
    state = serializers.CharField()
    country = serializers.CharField()
 
 
class AllOrdersSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderProduct
        fields = '__all__'   

class OrderHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderDetail
        fields = '__all__'


class TopProductSerializer(serializers.Serializer):
    product_name = serializers.CharField()
    total = serializers.IntegerField()


class OrderProductSerializer(serializers.ModelSerializer):
    order = OrderHistorySerializer()
    class Meta:
        model = OrderProduct
        fields = '__all__'

        
class OrderDetailSerializer(serializers.ModelSerializer):
    products = OrderProductSerializer(many=True)
    class Meta:
        model = OrderDetail
        fields = '__all__'


