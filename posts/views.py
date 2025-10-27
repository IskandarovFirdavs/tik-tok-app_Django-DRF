from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, status
from rest_framework.filters import SearchFilter
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND, HTTP_201_CREATED, HTTP_200_OK, HTTP_403_FORBIDDEN, HTTP_204_NO_CONTENT

from posts.models import PostModel, HashtagModel, MusicModel, LikeModel, CommentModel, CommentLikeModel, \
    CommentDislikeModel, ReplyModel, ReplyCommentLikeModel, ReplyCommentDislikeModel, NotificationModel
from posts.serializers import CommentLikeSerializer, PostModelSerializer, HashtagModelSerializer, MusicModelSerializer, \
    LikeModelSerializer, CommentModelSerializer, CommentDislikeSerializer, ReplyModelSerializer, \
    ReplyCommentLikeModelSerializer, ReplyCommentDislikeModelSerializer


class HashtagListView(viewsets.ModelViewSet):
    queryset = HashtagModel.objects.all()
    serializer_class = HashtagModelSerializer

    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ['name', ]
    filter_fields = ['name', ]


class MusicListView(viewsets.ModelViewSet):
    queryset = MusicModel.objects.all()
    serializer_class = MusicModelSerializer

    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ['singer', 'music_name']
    filter_fields = ['singer', 'music_name']


class PostViewSet(viewsets.ModelViewSet):
    queryset = PostModel.objects.all().order_by('-created_at')
    serializer_class = PostModelSerializer

    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ['title', 'hashtags__name']
    filter_fields = ['hashtag', 'music', 'user']
    permission_classes = (IsAuthenticatedOrReadOnly,)

    # Create post
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    # Retrieve post
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # Update post
    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()

        if instance.user != request.user and not request.user.is_staff:
            return Response(
                {'detail': 'Siz faqat o‘zingizga tegishli postni tahrirlay olasiz.'},
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)

    # Delete post
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        if instance.user != request.user and not request.user.is_staff:
            return Response(
                {'detail': 'Siz faqat o‘zingizning postingizni o‘chira olasiz.'},
                status=status.HTTP_403_FORBIDDEN
            )

        instance.delete()
        return Response({'detail': 'Post o‘chirildi.'}, status=status.HTTP_204_NO_CONTENT)
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context


class GenreListViewSet(viewsets.ViewSet):
    def list(self, request):
        genres = [
            {"value": choice[0], "label": choice[1]}
            for choice in PostModel.GenreChoice.choices
        ]
        return Response(genres, status=status.HTTP_200_OK)


class LikeViewSet(viewsets.ModelViewSet):
    queryset = LikeModel.objects.all()
    serializer_class = LikeModelSerializer
    permission_classes = (IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        user = request.user
        post_id = request.data.get('post')

        if not post_id:
            return Response({'detail': 'post did not find'}, status=HTTP_400_BAD_REQUEST)
        try:
            post = PostModel.objects.get(id=post_id)
            like = LikeModel.objects.filter(post=post, user=user).first()

            if like:
                like.delete()
                NotificationModel.objects.filter(sender=request.user, receiver=post.user, post=post,
                                                 notif_type=NotificationModel.NotifType.Like).delete()
                return Response({'liked': False, 'detail': 'Like is deleted'}, status=HTTP_200_OK)
            else:
                LikeModel.objects.create(post=post, user=user)
                NotificationModel.objects.create(sender=request.user, receiver=post.user, post=post,
                                                 notif_type=NotificationModel.NotifType.Like)

                return Response({'liked': True, 'detail': 'Like is created'}, status=HTTP_201_CREATED)
        except PostModel.DoesNotExist:
            return Response({'detail': 'post does not exist'}, status=HTTP_404_NOT_FOUND)


class CommentView(viewsets.ModelViewSet):
    queryset = CommentModel.objects.all()
    serializer_class = CommentModelSerializer
    permission_classes = (IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        user = request.user
        post_id = request.data.get('post')
        text = request.data.get('text')

        if not post_id or not text:
            return Response({'detail': 'post or text did not find'}, status=HTTP_400_BAD_REQUEST)
        try:
            post = PostModel.objects.get(id=post_id)
        except PostModel.DoesNotExist:
            return Response({'detail': 'post did not find'}, status=HTTP_404_NOT_FOUND)

        text = request.data.get('text')

        comment = CommentModel.objects.create(post=post, user=user, text=text)
        serializer = self.get_serializer(comment)
        return Response(serializer.data, status=HTTP_201_CREATED)

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()

        if instance.user != request.user and not request.user.is_staff:
            return Response(
                {'detail': 'Siz faqat o‘zingizga tegishli kommentni tahrirlay olasiz.'},
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        if instance.user != request.user and not request.user.is_staff:
            return Response({'detail': 'You can only delete your own comment'}, status=HTTP_403_FORBIDDEN)

        instance.delete()
        return Response({'detail': 'Comment deleted'}, status=HTTP_204_NO_CONTENT)


class CommentLikeViewSet(viewsets.ModelViewSet):
    queryset = CommentLikeModel.objects.all()
    serializer_class = CommentLikeSerializer
    permission_classes = (IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        user = request.user
        comment_id = request.data.get('comment')

        if not comment_id:
            return Response({'detail': 'Comment did not find'}, status=HTTP_400_BAD_REQUEST)
        try:
            comment = CommentModel.objects.get(id=comment_id)
            comment_like = CommentLikeModel.objects.filter(comment=comment, user=user)
            dislike = CommentDislikeModel.objects.filter(comment=comment, user=user)
            if dislike:
                dislike.delete()
                CommentLikeModel.objects.create(comment=comment, user=user)
                return Response({'detail': "Dislike removed and Comment liked successfully"}, status=HTTP_201_CREATED)
            elif comment_like:
                comment_like.delete()
                return Response({'detail': "Comment like removed successfully"}, status=HTTP_204_NO_CONTENT)

            CommentLikeModel.objects.create(comment=comment, user=user)
            return Response({'detail': "Comment liked successfully"}, status=HTTP_201_CREATED)


        except CommentModel.DoesNotExist:
            return Response({'detail': 'Comment did not exist'}, status=HTTP_404_NOT_FOUND)


class CommentDislikeViewSet(viewsets.ModelViewSet):
    queryset = CommentDislikeModel.objects.all()
    serializer_class = CommentDislikeSerializer
    permission_classes = (IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        user = request.user
        comment_id = request.data.get('comment')

        if not comment_id:
            return Response({'detail': 'Comment did not find'}, status=HTTP_400_BAD_REQUEST)
        try:                                
            comment = CommentModel.objects.get(id=comment_id)
            comment_like = CommentLikeModel.objects.filter(comment=comment, user=user)
            dislike = CommentDislikeModel.objects.filter(comment=comment, user=user)
            if comment_like:
                comment_like.delete()
                CommentDislikeModel.objects.create(comment=comment, user=user)
                return Response({'detail': "Like removed and Comment disliked successfully"}, status=HTTP_201_CREATED)
            elif dislike:
                dislike.delete()
                return Response({'detail': "Comment dislike removed successfully"}, status=HTTP_204_NO_CONTENT)
            
            CommentDislikeModel.objects.create(comment=comment, user=user)
            return Response({'detail': "Comment disliked successfully"}, status=HTTP_201_CREATED)
        except CommentModel.DoesNotExist:
            return Response({'detail': 'Comment did not exist'}, status=HTTP_404_NOT_FOUND)


class ReplyCommentView(viewsets.ModelViewSet):
    queryset = ReplyModel.objects.all()
    serializer_class = ReplyModelSerializer
    permission_classes = (IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        user = request.user
        post_id = request.data.get('post')
        comment_id = request.data.get('comment')
        text = request.data.get('text')

        if not comment_id or not text or not post_id:
            return Response({'detail':'post or comment or text did not find'}, status=HTTP_400_BAD_REQUEST)
        try:
            post = PostModel.objects.get(id=post_id)
            comment = CommentModel.objects.get(id=comment_id)
            text = request.data.get('text')
            reply_comment = ReplyModel.objects.create(user=user, comment=comment, post=post, text=text)
            serializer = self.get_serializer(reply_comment)
            return Response(serializer.data, status=HTTP_201_CREATED)
        except CommentModel.DoesNotExist:
            return Response({'detail':'comment did not exist'}, status=HTTP_404_NOT_FOUND)
        except PostModel.DoesNotExist:
            return Response({'detail':'post did not exist'}, status=HTTP_404_NOT_FOUND)

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()

        if request.user != instance.user or not request.user.is_staff:
            return Response({'detail':'You can delete only your reply comments'}, status=HTTP_403_FORBIDDEN)
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        if instance.user != request.user or not request.user.is_staff:
            return Response({'detail':'You can delete only your reply comments'}, status=HTTP_403_FORBIDDEN)
        instance.delete()
        return Response({"detail":'Reply comment deleted'}, status=HTTP_204_NO_CONTENT)


class ReplyCommentLikeView(viewsets.ModelViewSet):
    queryset = ReplyCommentLikeModel.objects.all()
    serializer_class = ReplyCommentLikeModelSerializer
    permission_classes = (IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        user = request.user
        reply_comment_id = request.data.get('reply_comment')

        if not reply_comment_id:
            return Response({'detail':'Reply comment did not find'}, status=HTTP_400_BAD_REQUEST)
        try:
            reply_comment = ReplyModel.objects.get(id=reply_comment_id)
            reply_comment_like = ReplyCommentLikeModel.objects.filter(reply_comment=reply_comment, user=user)
            dislike = ReplyCommentDislikeModel.objects.filter(reply_comment=reply_comment, user=user)
            if dislike:
                dislike.delete()
                ReplyCommentLikeModel.objects.create(reply_comment=reply_comment, user=user)
                return Response({'detail':'reply disliked and reply liked'}, status=HTTP_201_CREATED)
            elif reply_comment_like:
                reply_comment_like.delete()
                return Response({'detail':'reply like removed'}, status=HTTP_204_NO_CONTENT)

            ReplyCommentLikeModel.objects.create(reply_comment=reply_comment, user=user)
            return Response({'detail':'reply comment liked'}, status=HTTP_201_CREATED)
        except ReplyModel.DoesNotExist:
            return Response({'detail':'reply comment did not exist'}, status=HTTP_404_NOT_FOUND)


class ReplyCommentDislikeView(viewsets.ModelViewSet):
    queryset = ReplyCommentDislikeModel.objects.all()
    serializer_class = ReplyCommentDislikeModelSerializer
    permission_classes = (IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        user = request.user
        reply_comment_id = request.data.get('reply_comment')

        if not reply_comment_id:
            return Response({'detail': 'Reply comment did not find'}, status=HTTP_400_BAD_REQUEST)
        try:
            reply_comment = ReplyModel.objects.get(id=reply_comment_id)
            reply_comment_like = ReplyCommentLikeModel.objects.filter(reply_comment=reply_comment, user=user)
            dislike = ReplyCommentDislikeModel.objects.filter(reply_comment=reply_comment, user=user)
            if reply_comment_like:
                reply_comment_like.delete()
                ReplyCommentDislikeModel.objects.create(reply_comment=reply_comment, user=user)
                return Response({'detail': 'reply liked and reply disliked'},
                                status=HTTP_201_CREATED)
            elif dislike:
                dislike.delete()
                return Response({'detail': 'reply like removed'}, status=HTTP_204_NO_CONTENT)

            ReplyCommentDislikeModel.objects.create(reply_comment=reply_comment, user=user)
            return Response({'detail': 'reply comment disliked'}, status=HTTP_201_CREATED)
        except ReplyModel.DoesNotExist:
            return Response({'detail': 'reply comment did not exist'}, status=HTTP_404_NOT_FOUND)


