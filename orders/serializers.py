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
        
    def update(self, instance, validated_data):
        instance.order = validated_data.get('order', instance.order)
        instance.product = validated_data.get('product', instance.product)
        instance.product_name = validated_data.get('product_name', instance.product_name)
        instance.payment = validated_data.get('payment', instance.payment)
        instance.user = validated_data.get('user', instance.user)
        instance.color = validated_data.get('color', instance.color)
        instance.size = validated_data.get('size', instance.size)
        instance.brand = validated_data.get('brand', instance.brand)
        instance.price = validated_data.get('price', instance.price)
        instance.quantity = validated_data.get('quantity', instance.quantity)
        instance.total_amount = validated_data.get('total_amount', instance.total_amount)
        instance.status = validated_data.get('status', instance.status)
        
        return super().update(instance, validated_data)


class OrderUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderProduct
        fields = '__all__'
        
    def update(self, instance, validated_data):
        instance.order = validated_data.get('order', instance.order)
        instance.product = validated_data.get('product', instance.product)
        instance.product_name = validated_data.get('product_name', instance.product_name)
        instance.payment = validated_data.get('payment', instance.payment)
        instance.user = validated_data.get('user', instance.user)
        instance.color = validated_data.get('color', instance.color)
        instance.size = validated_data.get('size', instance.size)
        instance.brand = validated_data.get('brand', instance.brand)
        instance.price = validated_data.get('price', instance.price)
        instance.quantity = validated_data.get('quantity', instance.quantity)
        instance.total_amount = validated_data.get('total_amount', instance.total_amount)
        instance.status = validated_data.get('status', instance.status)
        
        return super().update(instance, validated_data)

        
class OrderDetailSerializer(serializers.ModelSerializer):
    products = OrderProductSerializer(many=True)
    class Meta:
        model = OrderDetail
        fields = '__all__'


