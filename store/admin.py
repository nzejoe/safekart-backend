from django.contrib import admin

from .models import Product, Variation, Category


class ProductAdmin(admin.ModelAdmin):
    model = Product
    list_display = ['product_name', 'category', 'stock', 'price', 'active']
    populated_fields = {'slug': ('product_name', )}
    

admin.site.register(Product, ProductAdmin)
admin.site.register(Variation)
admin.site.register(Category)
