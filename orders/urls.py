from django.urls import path

from . import views


urlpatterns = [
    path('place_order/', views.PlaceOrder.as_view(), name='place_order'),
    path('orders_history/', views.OrderHistory.as_view(), name='order_history'),
    path('<str:order_number>/', views.OrderDetailView.as_view(), name='order_detail'),
]
