# Create your views here.

from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from django.http import HttpResponse
from .models import Book, Library  # Assuming these models exist

# Function-based view to list all books
def list_books(request):
    books = Book.objects.all()
    return render(request, "relationship_app/list_books.html", {"books": books})


from django.views.generic.detail import DetailView

# Class-based view to display library details
class LibraryDetailView(DetailView):
    model = Library
    template_name = 'relationship_app/library_detail.html'
    context_object_name = 'library'
