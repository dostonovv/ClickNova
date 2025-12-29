# support/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.support_dashboard, name='support_dashboard'),
    path('order/<int:pk>/', views.support_order_detail, name='support_order_detail'),
]