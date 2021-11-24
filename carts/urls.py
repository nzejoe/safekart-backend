from django.urls import path

from . import views


urlpatterns = [
    path('', views.CartList.as_view(), name='cart_list'),
    path('add_to_cart/', views.AddToCart.as_view(), name='add_to_cart'),
]
