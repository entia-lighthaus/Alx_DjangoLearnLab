from django.db import models

# The Author model represents a book author.
# Each author has a name and can write many books.
class Author(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

# The Book model represents a book with a title and publication year.
# It has a ForeignKey to Author, creating a one-to-many relationship.
class Book(models.Model):
    title = models.CharField(max_length=200)
    publication_year = models.PositiveIntegerField()
    author = models.ForeignKey(Author, related_name='books', on_delete=models.CASCADE)

    def __str__(self):
        return self.title
