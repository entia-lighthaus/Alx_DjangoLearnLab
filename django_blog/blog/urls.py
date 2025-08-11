from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('profile/<str:username>/', views.profile_view, name='profile_view'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', views.custom_logout, name='logout'),
]