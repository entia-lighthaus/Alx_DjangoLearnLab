# relationship_app/urls.py
# Create this file in your relationship_app directory
from .views import list_books, LibraryDetailView, LibraryListView

urlpatterns = [
    path('books/', list_books, name='list_books'),
    path('library/<int:pk>/', LibraryDetailView.as_view(), name='library_detail'),
    path('libraries/', LibraryListView.as_view(), name='library_list'),
]
