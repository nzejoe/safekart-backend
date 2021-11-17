from django.urls import path

from . import views


urlpatterns = [
    path('login/', views.UserLogin.as_view(), name='login'),
    path('logout/', views.UserLogout.as_view(), name='logout'),
    path('register/', views.UserRegister.as_view(), name='register'),
    path('password_reset/', views.PasswordReset.as_view(), name='password_reset'),
    path('password_reset_confirm/<uidb64>/<token>/',views.PasswordResetConfirm.as_view(), name='password_reset_confirm'),
    path('password_reset_complete/',views.PasswordResetComplete.as_view(), name='password_reset_complete'),
    path('password_reset_change/',views.PasswordChange.as_view(), name='password_change'),
]
