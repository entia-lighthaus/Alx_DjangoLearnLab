from rest_framework import serializers
from .models import Post, Comment


# Serializer for Comment model
# Serializers convert Django model objects into JSON (for API responses) and back into Python objects (for requests)
class CommentSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'post', 'author', 'content', 'created_at', 'updated_at']
        read_only_fields = ['author', 'created_at', 'updated_at']


class PostSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True) # Display username instead of user ID
    comments = CommentSerializer(many=True, read_only=True) # Nested serializer to include comments in the post response

    class Meta:
        model = Post
        fields = ['id', 'author', 'title', 'content', 'created_at', 'updated_at', 'comments']
        read_only_fields = ['author', 'created_at', 'updated_at']
