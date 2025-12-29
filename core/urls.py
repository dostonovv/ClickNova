# core/urls.py — FINAL SODDA VERSIYA
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),  # bosh sahifa
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),  # o‘zimizning login view
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'), # <--- MANA SHU!
    path('profile/', views.profile, name='profile'),
]