from django.contrib.auth.decorators import user_passes_test, login_required
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import DetailView
from django.http import HttpResponse, HttpResponseForbidden
from .models import Book, Library, UserProfile
from django.core.exceptions import PermissionDenied
from django.contrib.auth.views import LoginView
from django.contrib.auth import authenticate, login as auth_login


def is_admin(user):
    """
    Check if the user has Admin role.
    """
    if not user.is_authenticated:
        return False
    try:
        return user.userprofile.role == 'Admin'
    except UserProfile.DoesNotExist:
        return False


def is_librarian(user):
    """
    Check if the user has Librarian role.
    """
    if not user.is_authenticated:
        return False
    try:
        return user.userprofile.role == 'Librarian'
    except UserProfile.DoesNotExist:
        return False


def is_member(user):
    """
    Check if the user has Member role.
    """
    if not user.is_authenticated:
        return False
    try:
        return user.userprofile.role == 'Member'
    except UserProfile.DoesNotExist:
        return False


# Home view that redirects based on user role
@login_required
def home_view(request):
    """
    Home view that redirects users based on their role.
    """
    if hasattr(request.user, 'userprofile'):
        role = request.user.userprofile.role
        if role == 'Admin':
            return redirect('admin_view')
        elif role == 'Librarian':
            return redirect('librarian_view')
        elif role == 'Member':
            return redirect('member_view')
    
    return render(request, 'relationship_app/home.html')


@login_required
@user_passes_test(is_admin, login_url='/access_denied/')
def admin_view(request):
    """
    View accessible only to users with Admin role.
    """
    context = {
        'user_role': request.user.userprofile.role,
        'page_title': 'Admin Dashboard',
        'welcome_message': f'Welcome, {request.user.username}! You have admin access.',
    }
    return render(request, 'relationship_app/admin_view.html', context)


@login_required
@user_passes_test(is_librarian, login_url='/access_denied/')
def librarian_view(request):
    """
    View accessible only to users with Librarian role.
    """
    context = {
        'user_role': request.user.userprofile.role,
        'page_title': 'Librarian Dashboard',
        'welcome_message': f'Welcome, {request.user.username}! You have librarian access.',
    }
    return render(request, 'relationship_app/librarian_view.html', context)


@login_required
@user_passes_test(is_member, login_url='/access_denied/')
def member_view(request):
    """
    View accessible only to users with Member role.
    """
    context = {
        'user_role': request.user.userprofile.role,
        'page_title': 'Member Dashboard',
        'welcome_message': f'Welcome, {request.user.username}! You have member access.',
    }
    return render(request, 'relationship_app/member_view.html', context)


def access_denied(request):
    """
    View to handle access denied scenarios.
    """
    context = {
        'message': 'Access Denied: You do not have permission to view this page.',
    }
    return render(request, 'relationship_app/access_denied.html', context, status=403)


# Note: Using Django's built-in LoginView and LogoutView from urls.py


# Registration view
def register(request):
    """
    User registration view.
    """
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Create a default UserProfile with Member role
            UserProfile.objects.create(user=user, role='Member')
            auth_login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'relationship_app/register.html', {'form': form})


# Book list
def list_books(request):
    """
    List all books.
    """
    books = Book.objects.all()
    return render(request, "relationship_app/list_books.html", {"books": books})


# Library detail view
class LibraryDetailView(DetailView):
    """
    Detail view for library.
    """
    model = Library
    template_name = 'relationship_app/library_detail.html'
    context_object_name = 'library'