from django.urls import path

from . import views


urlpatterns = [
    path('place_order/', views.PlaceOrder.as_view(), name='place_order'),
]
