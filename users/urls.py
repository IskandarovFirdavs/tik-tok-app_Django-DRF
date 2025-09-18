from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (
    UserListCreateView,
    UserDetailView,
    LoginView,
    CurrentUserView,
)


urlpatterns = [
    path('login/', LoginView.as_view(), name='custom_login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('', UserListCreateView.as_view(), name='users_users_list'),
    path('<int:pk>/', UserDetailView.as_view(), name='users_users_detail'),
    path('me/', CurrentUserView.as_view(), name='users_users_me'),
]