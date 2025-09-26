from django.urls import path
from rest_framework.routers import DefaultRouter

from posts import views

router = DefaultRouter()
router.register(r'post', views.PostViewSet)
router.register(r'hashtags', views.HashtagListView)

urlpatterns = [
]

urlpatterns += router.urls
