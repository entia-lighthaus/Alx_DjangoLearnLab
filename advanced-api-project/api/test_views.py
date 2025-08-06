from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Book, Author

class BookAPITestCase(APITestCase):
    def setUp(self):
        # Create user and token
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.login(username='testuser', password='testpass')

        # Create an author
        self.author = Author.objects.create(name="Chinua Achebe")

        # Create some books
        self.book1 = Book.objects.create(title="Things Fall Apart", publication_year=1958, author=self.author)
        self.book2 = Book.objects.create(title="No Longer at Ease", publication_year=1960, author=self.author)

    def test_list_books(self):
        response = self.client.get(reverse('book-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_create_book(self):
        data = {
            'title': 'Arrow of God',
            'publication_year': 1964,
            'author': self.author.id
        }
        response = self.client.post(reverse('book-create'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 3)

    def test_update_book(self):
        data = {'title': 'Updated Title'}
        response = self.client.patch(reverse('book-update', kwargs={'pk': self.book1.pk}), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book1.refresh_from_db()
        self.assertEqual(self.book1.title, 'Updated Title')

    def test_delete_book(self):
        response = self.client.delete(reverse('book-delete', kwargs={'pk': self.book2.pk}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), 1)

    def test_filter_books_by_year(self):
        response = self.client.get(reverse('book-list') + '?publication_year=1958')
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Things Fall Apart')

    def test_search_books(self):
        response = self.client.get(reverse('book-list') + '?search=Ease')
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'No Longer at Ease')

    def test_order_books_by_title(self):
        response = self.client.get(reverse('book-list') + '?ordering=title')
        titles = [book['title'] for book in response.data]
        self.assertEqual(titles, sorted(titles))

    def test_permission_required_for_create(self):
        self.client.logout()
        data = {
            'title': 'New Unauthorized Book',
            'publication_year': 2025,
            'author': self.author.id
        }
        response = self.client.post(reverse('book-create'), data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


## API Test Coverage

#List all books (`GET /api/books/`)
#Create a book (`POST /api/books/create/`)
#Update a book (`PATCH /api/books/update/<id>/`)
#Delete a book (`DELETE /api/books/delete/<id>/`)
#Filter by publication_year
#Search by title/author
#Order by title/year
#Test permission enforcement
