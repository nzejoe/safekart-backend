from django.db import models

from accounts.models import Account
from store.models import Product


class ItemVariation(models.Model):
    variation_id = models.CharField(max_length=100)
    color = models.CharField(max_length=20, null=True, blank=True)
    size = models.CharField(max_length=20, null=True, blank=True)
    brand = models.CharField(max_length=20, null=True, blank=True)
    
    def __str__(self):
        return f'{self.color}-{self.size}-{self.brand}'


class Cart(models.Model):
    cart_id = models.CharField(max_length=100, unique=True)
    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.cart_id
    

class Cartitem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    user = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variation = models.ForeignKey(ItemVariation, on_delete=models.CASCADE, related_name='item')
    quantity = models.IntegerField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.product.product_name



"""[summary]
    Cart model: cart models will be used to identify a user's cart whether authenticated or not, whenever they add item to their cart.
"""
    
    
