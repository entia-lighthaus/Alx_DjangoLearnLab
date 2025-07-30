# This API uses Token Authentication.
# Users must obtain a token via /api/auth/token/ by providing username/password.
# All BookViewSet routes are protected using IsAuthenticated permission class.

from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from rest_framework import generics
from .models import Book
from .serializers import BookSerializer



# ViewSets simplifies things by combining listing, creating, retrieving, updating, and deleting into one class. 
class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]



class BookList(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer



