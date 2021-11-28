from django.db import models

from accounts.models import Account
from carts.models import Product


class Payment(models.Model):
    payment_id = models.CharField(max_length=100)
    user = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True)
    amount = models.DecimalField(decimal_places=2, max_digits=20)
    payment_method = models.CharField(max_length=20)
    status = models.CharField(max_length=20)
    created = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.user.username


class OrderDetail(models.Model):
    order_number = models.CharField(max_length=100)
    payment = models.ForeignKey(Payment, on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True, related_name='orders')
    first_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50, null=True, blank=True)
    last_name = models.CharField(max_length=50)
    gender = models.CharField(max_length=10)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    address_1 = models.CharField(max_length=100)
    address_2 = models.CharField(max_length=100)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    tax = models.DecimalField(max_digits=20, decimal_places=2)
    total_amount = models.DecimalField(max_digits=20, decimal_places=2)
    grand_total = models.DecimalField(max_digits=20, decimal_places=2)
    is_ordered = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    
    def __str__(self):
        return f'{self.first_name} {self.last_name}'
    

class OrderProduct(models.Model):
    order = models.ForeignKey(OrderDetail, on_delete=models.CASCADE, related_name='products')
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    product_name = models.CharField(max_length=100, blank=True, null=True)
    payment = models.ForeignKey(Payment, on_delete=models.SET_NULL, null=True, related_name='products')
    user = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True, related_name='ordered_products')
    color = models.CharField(max_length=10, null=True, blank=True)
    size = models.CharField(max_length=10, null=True, blank=True)
    brand = models.CharField(max_length=10, null=True, blank=True)
    price = models.DecimalField(max_digits=20, decimal_places=2)
    quantity = models.IntegerField()
    total_amount = models.DecimalField(max_digits=20, decimal_places=2)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):
        self.total_amount = self.quantity * self.price
        self.product_name = self.product.product_name
        return super(OrderProduct, self).save(*args, **kwargs)
    
    def __str__(self):
        return self.product.product_name
    
