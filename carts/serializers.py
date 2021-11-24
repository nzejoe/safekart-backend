from rest_framework import serializers

from .models import Cartitem


class CartSerializer(serializers.Serializer):
    product_id = serializers.UUIDField(required=True)
    color = serializers.CharField(allow_null=True, allow_blank=True)
    size = serializers.CharField(allow_null=True, allow_blank=True)
    brand = serializers.CharField(allow_null=True, allow_blank=True)
    
    
class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cartitem
        fields = '__all__'
