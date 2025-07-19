# relationship_app/urls.py
# Create this file in your relationship_app directory


from django.contrib.auth import views as auth_views
from . import views

from django.urls import path
from .views import list_books, LibraryDetailView
# from .views import LibraryListView  # Commented out for now


urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='relationship_app/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', register, name='register'),
]

urlpatterns = [
    path('books/', list_books, name='list_books'),
    path('library/<int:pk>/', LibraryDetailView.as_view(), name='library_detail'),
]



