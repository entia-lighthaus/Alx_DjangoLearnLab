from rest_framework import serializers
from .models import Book  # Assuming Book model is defined in models.py

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'  # This includes all fields of the Book model
