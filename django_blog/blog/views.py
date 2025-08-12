from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.contrib.auth.models import User
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .forms import CustomUserCreationForm, UserUpdateForm, ProfileUpdateForm, PostForm
from .models import Post, Profile


# authentication views
def home(request):
    posts = Post.objects.all()[:5]  # Get latest 5 posts
    return render(request, 'blog/home.html', {'posts': posts})

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}! You can now log in.')
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'blog/register.html', {'form': form})

@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, 'Your profile has been updated!')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
    
    context = {
        'u_form': u_form,
        'p_form': p_form,
        'user_posts': Post.objects.filter(author=request.user)
    }
    return render(request, 'blog/profile.html', context)

def profile_view(request, username):
    """View for displaying a user's public profile"""
    user = get_object_or_404(User, username=username)
    user_posts = Post.objects.filter(author=user)
    
    context = {
        'profile_user': user,
        'user_posts': user_posts,
        'is_own_profile': request.user == user if request.user.is_authenticated else False
    }
    return render(request, 'blog/profile_view.html', context)

def custom_logout(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully!')
    return render(request, 'registration/logged_out.html')



# Blog Post CRUD Views
class PostListView(ListView): # List all blog posts
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    ordering = ['-published_date']
    paginate_by = 5
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'All Blog Posts'
        return context

class PostDetailView(DetailView): # View a single blog post
    # This view displays the details of a single blog post.
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'

class PostCreateView(LoginRequiredMixin, CreateView): # Create a new blog post
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(self.request, 'Your post has been created successfully!')
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Create New Post'
        context['button_text'] = 'Create Post'
        return context

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView): # Update an existing blog post
    # This view allows the author to edit their blog post.
    # It checks if the user is the author before allowing updates.
    # If the user is not the author, they will be redirected to a 403 Forbidden page.
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'
    
    def form_valid(self, form):
        messages.success(self.request, 'Your post has been updated successfully!')
        return super().form_valid(form)
    
    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edit Post'
        context['button_text'] = 'Update Post'
        return context

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView): # Delete a blog post
    # This view allows the author to delete their blog post.
    # It checks if the user is the author before allowing deletion.
    # If the user is not the author, they will be redirected to a 403 Forbidden page.
    # After deletion, a success message is displayed.
    model = Post
    template_name = 'blog/post_confirm_delete.html'
    context_object_name = 'post'
    success_url = reverse_lazy('post-list')
    
    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Your post has been deleted successfully!')
        return super().delete(request, *args, **kwargs)