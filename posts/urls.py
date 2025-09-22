from django.urls import path
from posts import views

urlpatterns = [
    path('create/', views.PostCreateAPIView.as_view(), name='create'),
    path('posts/', views.PostListAPIView.as_view(), name='posts')
]
