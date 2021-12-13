import uuid

from django.db import models
from django.utils.text import slugify
from PIL import Image
from imagekit.models import ImageSpecField, ProcessedImageField
from imagekit.processors import ResizeToFill

from accounts.models import Account

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    image = models.ImageField(upload_to='category', null=True, blank=True)
    description = models.CharField(max_length=200, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    
    
    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
    
    
    def __str__(self):
        return self.name


class Product(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    product_name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(unique=True, null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='category')
    image = models.ImageField(upload_to='products', null=True, blank=True)
    description = models.TextField()
    price = models.DecimalField(decimal_places=2, max_digits=19)
    stock = models.IntegerField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.product_name
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        
        self.slug = slugify(self.product_name, allow_unicode=True)
        
        # get this product image
        img = Image.open(self.image.path)
        
        # check if image is greater than 500px
        if img.width > 500 or img.height > 500:
            # set default output size
            output_size = (500, 500)
            img.thumbnail(output_size)
            img.save(self.image.path) # overwrite the image


class ProductGallery(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='gallery')
    image = ProcessedImageField(
        upload_to='products/gallery', processors=[ResizeToFill(500, 500), ], format='JPEG', options={'quality': 60})
    thumb = ImageSpecField(source='image', processors=[ResizeToFill(
        100, 100), ],  format='JPEG', options={'quality': 60})
    
    class Meta:
        verbose_name = 'gallery'
        verbose_name_plural = 'galleries'
        
    
    def __str__(self):
        return self.product.product_name
        


class VariationManager(models.Manager):
    
    def colors(self):
        return super(VariationManager, self).filter(variation_category='color')
    
    def sizes(self):
        return super(VariationManager, self).filter(variation_category='size')


class Variation(models.Model):
    CATEGORY = (
        ('color', 'Color'),
        ('size', 'Size'),
        ('brand', 'Brand'),
    )
    
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='variations')
    variation_category = models.CharField(choices=CATEGORY, max_length=50) 
    variation_value = models.CharField(max_length=50)
    created = models.DateTimeField(auto_now_add=True)

    variations = VariationManager()
    
    def __str__(self):
        return self.product.product_name


class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='reviews')
    subject = models.CharField(max_length=100, blank=True, null=True)
    review = models.TextField(blank=True, null=True)
    rating = models.FloatField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    
    def __str__(self):
        return self.subject
