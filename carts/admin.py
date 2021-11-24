from django.contrib import admin

from .models import Cart, ItemVariation, Cartitem


admin.site.register(Cart)
admin.site.register(ItemVariation)
admin.site.register(Cartitem)
