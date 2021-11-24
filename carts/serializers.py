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
    
    
class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer()
    variation = ItemVariationSerializer()
    class Meta:
        model = Cartitem
        fields = '__all__'
