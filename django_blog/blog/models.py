from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from PIL import Image
from django.urls import reverse 

# Blog Post Model
# This model represents a blog post in the application.
# It includes fields for the post title, content, published date, and author.
# The title is a CharField with a maximum length of 200 characters.
class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    published_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk}) # URL for the post detail view
    
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



# User Profile Model
# This model extends the User model to include additional fields for user profiles.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)

    # profile_picture: ImageField to store user's profile picture
    # default='default.jpg': Use a default image if none is uploaded
    profile_picture = models.ImageField(default='profile_pics/default.jpg', upload_to='profile_pics')
    website = models.URLField(max_length=200, blank=True)
    
    def __str__(self):
        return f"{self.user.username}'s Profile"
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        
        # Resize image if it's too large
        img = Image.open(self.profile_picture.path)
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.profile_picture.path)

# Create a profile automatically when a user is created
@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()