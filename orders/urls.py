from django.urls import path

from . import views


urlpatterns = [
    path('', views.OrderHistory.as_view(), name="orders"),
    path('order_update/<int:pk>/',views.OrderUpdate.as_view(), name='order_update'),
    path('top_selling/', views.TopSelling.as_view(), name='top_selling'),
    path('place_order/', views.PlaceOrder.as_view(), name='place_order'),
    path('order_history/', views.UserOrderHistory.as_view(), name='order_history'),
    path('<str:order_number>/', views.OrderDetailView.as_view(), name='order_detail'),
]
