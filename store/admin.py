from django.contrib import admin

from .models import Product, Variation, Category, Review, ProductGallery


class ReviewInline(admin.TabularInline):
    model = Review
    extra = 0
    readonly_fields = ['review','user', 'rating', 'subject', 'created', 'updated']


class GalleryAdmin(admin.ModelAdmin):
    model = ProductGallery
    fields = ['product', 'image']  
    
class GalleryInline(admin.TabularInline):
    model = ProductGallery
    extra = 0
    readonly_fields = ['image', 'thumb']

class ProductAdmin(admin.ModelAdmin):
    model = Product
    list_display = ['product_name', 'category', 'stock', 'price', 'active']
    populated_fields = {'slug': ('product_name', )}
    inlines = [GalleryInline, ReviewInline, ]
    

admin.site.register(Product, ProductAdmin)
admin.site.register(Variation)
admin.site.register(Category)
admin.site.register(Review)
admin.site.register(ProductGallery, GalleryAdmin)
