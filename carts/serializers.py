from rest_framework import serializers

from store.serializers import ProductSerializer
from .models import Cartitem, ItemVariation


class ItemVariationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemVariation
        fields = '__all__'


class CartSerializer(serializers.Serializer):
    product_id = serializers.UUIDField(required=True)
    color = serializers.CharField(allow_null=True, allow_blank=True)
    size = serializers.CharField(allow_null=True, allow_blank=True)
    brand = serializers.CharField(allow_null=True, allow_blank=True)
    quantity = serializers.IntegerField()
    
    
class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer()
    variation = ItemVariationSerializer()
    total_amount = serializers.SerializerMethodField(method_name='get_total_amount')
    class Meta:
        model = Cartitem
        fields = '__all__'
        
    
    def get_total_amount(self, object):
        price = object.product.price
        quantity = object.quantity
        amount = price * quantity
        return amount
