from rest_framework import serializers
from datetime import datetime
from .models import Author, Book

# Serializer for the Book model.
# It serializes all fields and includes a custom validator to ensure
# the publication_year is not in the future.
class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'

    def validate_publication_year(self, value):
        current_year = datetime.now().year
        if value > current_year:
            raise serializers.ValidationError("Publication year cannot be in the future.")
        return value

# Serializer for the Author model.
# Includes a nested list of books using BookSerializer.
class AuthorSerializer(serializers.ModelSerializer):
    # Nested serializer to show books by this author
    books = BookSerializer(many=True, read_only=True)

    class Meta:
        model = Author
        fields = ['id', 'name', 'books']
