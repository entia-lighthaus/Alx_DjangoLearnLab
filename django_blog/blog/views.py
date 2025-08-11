from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from .forms import CustomUserCreationForm, UserUpdateForm, ProfileUpdateForm
from .models import Post, Profile

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