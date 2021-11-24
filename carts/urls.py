from django.urls import path

from . import views


urlpatterns = [
    path('', views.CartList.as_view(), name='cart_list'),
    path('add_to_cart/', views.AddToCart.as_view(), name='add_to_cart'),
    path('increment_item/', views.IncrementCartItem.as_view(), name='increment_item'),
    path('decrement_item/', views.DecrementCartItem.as_view(), name='decrement_item'),
    path('remove_item/', views.RemoveCartItem.as_view(), name='remove_item'),
]
