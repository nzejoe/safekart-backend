from django.urls import path

from . import views

urlpatterns = [
    path('', views.ProductList.as_view(), name='product_list'),
    path('add_review/', views.AddReview.as_view(), name='add_review'),
    path('<str:slug>/', views.ProductDetail.as_view(), name='product_detail'),
]
