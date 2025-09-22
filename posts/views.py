from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny

from posts.models import PostModel
from posts.serializers import PostModelSerializer, PostModelCreateSerializer


class PostCreateAPIView(CreateAPIView):
    queryset = PostModel.objects.all()
    serializer_class = PostModelCreateSerializer
    permission_classes = [IsAuthenticated]


class PostListAPIView(ListAPIView):
    queryset = PostModel.objects.all().order_by("-created_at")
    serializer_class = PostModelSerializer
    permission_classes = [AllowAny]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context
