from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, RegisterView, LoginView, ProfileView

router = DefaultRouter()
router.register(r'users', UserViewSet)



urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('profile/', ProfileView.as_view(), name='profile'),

    path('unfollow/<int:user_id>/', UserViewSet.as_view({'post': 'unfollow'}), name='unfollow-user'),
    path('follow/<int:user_id>/', UserViewSet.as_view({'post': 'follow'}), name='follow-user'),

]

urlpatterns += router.urls

