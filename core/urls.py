# core/urls.py
from django.urls import path
from . import views
from .views import chart_view
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("", views.index, name="index"),
    path('calculator/', views.crypto_calculator, name='calculator'),
    path('chart/', chart_view, name='chart'),
    path('watch/', views.create_price_watch, name='create_price_watch'),
    path('watch/success/', views.watch_success, name='price_watch_success'),
    path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('accounts/password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('accounts/reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(),
         name='password_reset_confirm'),
    path('accounts/register/', views.register, name='register'),
    path('api/notifications/', views.api_notifications, name='api_notifications'),
    path('watch/delete/<int:watch_id>/', views.delete_price_watch, name='delete_price_watch'),
]
