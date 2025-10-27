from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (
    UserListCreateView,
    UserDetailView,
    LoginView,
    CurrentUserView,
    FollowToggleView,
    LogoutView,
)

urlpatterns = [
    path('login/', LoginView.as_view(), name='custom_login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('', UserListCreateView.as_view(), name='user_list'),
    path('<int:pk>/', UserDetailView.as_view(), name='user_detail'),
    path('me/', CurrentUserView.as_view(), name='user_me'),
    path('follow/<int:user_id>/', FollowToggleView.as_view(), name='follow_toggle'),
]
