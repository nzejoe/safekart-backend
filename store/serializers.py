from rest_framework import serializers

from .models import Category, Product, Review, Variation, ProductGallery


class VariationsSerializer(serializers.ModelSerializer):
    color_variation = serializers.SerializerMethodField(method_name='get_color_variation')
    
    class Meta:
        model = Variation
        fields = '__all__'
 
 
class ReviewSerialzer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    class Meta:
        model = Review
        fields = "__all__"
        

class GallerySerialzer(serializers.ModelSerializer):
    thumb = serializers.SerializerMethodField(method_name='get_thumb')
    class Meta:
        model = ProductGallery
        fields = ['image', 'thumb']
        
    
    def get_thumb(self, obj):
        return obj.thumb.url
    

class ProductSerializer(serializers.ModelSerializer):
    category = serializers.StringRelatedField(read_only=True)
    variations = VariationsSerializer(read_only=True, many=True)
    gallery = GallerySerialzer(many=True, read_only=True)
    
    variations = serializers.SerializerMethodField(method_name='get_variations')
    reviews = ReviewSerialzer(many=True, read_only=True)
    rating = serializers.SerializerMethodField(method_name='get_average_rating')
    
    class Meta:
        model = Product
        fields = ['id', 'product_name','slug', 'category',
                  'description', 'image', 'price', 'stock', 'created', 'updated', 'active', 'variations', 'reviews', 'gallery', 'rating']

    def get_variations(self, object):
        variations = {}
        colors = []
        sizes = []
        brands = []
        
        color_variations = object.variations.colors()
        size_variations = object.variations.sizes()
        brand_variations = object.variations.filter(variation_category='brand')
        
        if color_variations:
            for color in color_variations:
                colors.append(color.variation_value)
                
        if size_variations:
            for size in size_variations:
                sizes.append(size.variation_value)
                
        if brand_variations:
            for brand in brand_variations:
                brands.append(brand.variation_value)
        
        variations['colors'] = colors
        variations['sizes'] = sizes
        variations['brand'] = brands

        return variations


    def get_average_rating(self, object):
        reviews = object.reviews.all()
        total = 0
        count = 0
        average = 0
        for review in reviews:
            if review.rating:
                count += 1
                total += review.rating
        if count:
            average = total/count
        return round(average, 2)


class TopProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'
        
        
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'