from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, permissions
from rest_framework.filters import SearchFilter
from rest_framework.generics import ListAPIView

from posts.models import PostModel, HashtagModel
from posts.serializers import PostModelSerializer, HashtagModelSerializer


class PostViewSet(viewsets.ModelViewSet):
    queryset = PostModel.objects.order_by('-created_at')
    serializer_class = PostModelSerializer

    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ['title', 'hashtags__name']
    filter_fields = ['hashtag', 'music']

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [permissions.IsAuthenticated()]
        return []


class HashtagListView(viewsets.ModelViewSet):
    queryset = HashtagModel.objects.all()
    serializer_class = HashtagModelSerializer

    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ['name',]
    filter_fields = ['name',]

