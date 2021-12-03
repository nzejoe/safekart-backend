from django.urls import path

from . import views

urlpatterns = [
    path('', views.ProductList.as_view(), name='product_list'),
    path('add_review/', views.AddReview.as_view(), name='add_review'),
    path('update_review/<int:pk>/', views.UpdateReview.as_view(), name='update_review'),
    path('delete_review/<int:pk>/', views.DeleteReview.as_view(), name='delete_review'),
    path('<str:slug>/', views.ProductDetail.as_view(), name='product_detail'),
]
