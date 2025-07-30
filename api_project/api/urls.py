# api/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BookList, BookViewSet

# Set up router
router = DefaultRouter()
router.register(r'books_all', BookViewSet, basename='book_all')

urlpatterns = [
    # Old endpoint (ListAPIView)
    path('books/', BookList.as_view(), name='book-list'),

    # All CRUD routes via router
    path('', include(router.urls)),


]
