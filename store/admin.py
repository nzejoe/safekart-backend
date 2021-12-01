from django.contrib import admin

from .models import Product, Variation, Category, Review


class ReviewInline(admin.TabularInline):
    model = Review
    extra = 0
    readonly_fields = ['review','user', 'rating', 'subject', 'created', 'updated']

class ProductAdmin(admin.ModelAdmin):
    model = Product
    list_display = ['product_name', 'category', 'stock', 'price', 'active']
    populated_fields = {'slug': ('product_name', )}
    inlines = [ReviewInline, ]
    

admin.site.register(Product, ProductAdmin)
admin.site.register(Variation)
admin.site.register(Category)
admin.site.register(Review)
