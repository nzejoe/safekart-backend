from django.urls import path

from . import views

urlpatterns = [
    path('', views.ProductList.as_view(), name='product_list'),
    path('<uuid:pk>/', views.ProductDetail.as_view(), name='product_detail'),
]
