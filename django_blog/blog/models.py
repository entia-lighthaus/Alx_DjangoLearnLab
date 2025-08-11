from django.db import models
from django.contrib.auth.models import User

class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    published_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')
    
    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['-published_date']  # Show newest posts first



# title: CharField with max 200 characters for the blog post title
# content: TextField for the main blog post content (unlimited length)
# published_date: DateTimeField that automatically sets the date/time when a post is created
# author: ForeignKey linking to Django's built-in User model
# on_delete=models.CASCADE: If a user is deleted, their posts are also deleted
# related_name='blog_posts': Allows you to access a user's posts with user.blog_posts.all()
# __str__: Returns the title when the model is printed (useful in Django admin)
# Meta.ordering: Orders posts by newest first (the - means descending order)