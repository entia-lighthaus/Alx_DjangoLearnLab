from django.shortcuts import render
from rest_framework import viewsets,generics, permissions
from rest_framework.exceptions import PermissionDenied
from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer
from rest_framework import filters



class IsOwnerOrReadOnly(permissions.BasePermission):
    #Custom permission so users can only edit/delete their own content.

    def has_object_permission(self, request, view, obj):
        return obj.author == request.user or request.method in permissions.SAFE_METHODS



# Post viewset
# Enable search and ordering
class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().order_by('-created_at')
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'content']
    ordering_fields = ['created_at']

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


    

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all().order_by('-created_at')
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)



# Feed view
# This view returns posts from users that the current user follows.
class FeedView(generics.ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Get users current user follows
        followed_users = self.request.user.following.all()
        # Return posts from followed users
        return Post.objects.filter(author__in=followed_users).order_by #('-created_at')

