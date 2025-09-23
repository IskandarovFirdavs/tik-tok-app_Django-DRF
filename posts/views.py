from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, permissions
from rest_framework.filters import SearchFilter

from posts.models import PostModel
from posts.serializers import PostModelSerializer


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
