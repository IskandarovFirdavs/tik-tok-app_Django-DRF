from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, permissions
from rest_framework.filters import SearchFilter
from rest_framework.generics import ListAPIView
from posts.models import PostModel, HashtagModel, MusicModel
from posts.serializers import PostModelSerializer, HashtagModelSerializer, MusicModelSerializer


class HashtagListView(viewsets.ModelViewSet):
    queryset = HashtagModel.objects.all()
    serializer_class = HashtagModelSerializer

    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ['name',]
    filter_fields = ['name',]


class MusicListView(viewsets.ModelViewSet):
    queryset = MusicModel.objects.all()
    serializer_class = MusicModelSerializer

    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ['singer','music_name']
    filter_fields = ['singer','music_name']


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

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
