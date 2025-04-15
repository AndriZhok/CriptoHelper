# core/urls.py
from django.urls import path
from . import views
from .views import chart_view

urlpatterns = [
    path('calculator/', views.crypto_calculator, name='calculator'),
    path('chart/', chart_view, name='chart'),
]
