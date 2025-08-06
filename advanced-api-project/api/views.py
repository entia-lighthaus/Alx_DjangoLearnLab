from rest_framework import generics, filters
from django_filters import rest_framework
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated, AllowAny
from .models import Book
from .serializers import BookSerializer


"""
This module contains generic views for handling Book CRUD operations
using Django REST Framework.
"""

# Each view is designed to handle a specific operation.
# Permissions are enforced to allow only authenticated users to write data.

# Purpose: List all books (Read-only, accessible to all)
class BookListView(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]  # Public view


    """
BookListView:
- Supports filtering by 'title', 'author', 'publication_year'
    Example: ?publication_year=2023
- Supports searching by 'title' and 'author name'
    Example: ?search=python
- Supports ordering by 'title' and 'publication_year'
    Example: ?ordering=title or ?ordering=-publication_year
"""

    # Add filtering, search, and ordering support
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]

    # Fields users can filter by using ?field=value
    filterset_fields = ['title', 'author', 'publication_year']

    # Fields that will be searched via ?search=value
    search_fields = ['title', 'author__name']

    # Fields that can be sorted using ?ordering=field or ?ordering=-field
    ordering_fields = ['title', 'publication_year']

# Purpose: Retrieve a single book by ID
class BookDetailView(generics.RetrieveAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]  # Public view

# Purpose: Create a new book (Authenticated only)
class BookCreateView(generics.CreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]  # Only logged-in users can create

# Purpose: Update an existing book (Authenticated only)
class BookUpdateView(generics.UpdateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]  # Only logged-in users can update

# Purpose: Delete a book (Authenticated only)
class BookDeleteView(generics.DestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]  # Only logged-in users can delete
