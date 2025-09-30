from rest_framework import serializers
from posts.models import PostModel, HashtagModel, MusicModel, LikeModel, CommentModel, CommentLikeModel, ReplyModel, \
    ReplyCommentLikeModel, ViewModel, NotificationModel
from users.serializers import UserSerializer


class HashtagModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = HashtagModel
        fields = "__all__"


class MusicModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = MusicModel
        fields = "__all__"


class PostModelSerializer(serializers.ModelSerializer):
    post = serializers.SerializerMethodField()
    user = UserSerializer(read_only=True)
    music = MusicModelSerializer(read_only=True)
    hashtags = HashtagModelSerializer(read_only=True, many=True)

    def get_post(self, obj):
        request = self.context.get('request')
        if obj.post and request:
            return request.build_absolute_uri(obj.post.url)
        return obj.post.url if obj.post else None


    class Meta:
        model = PostModel
        fields = "__all__"


class LikeModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = LikeModel
        fields = "__all__"


class CommentModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommentModel
        fields = "__all__"


class CommentLikeModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommentLikeModel
        fields = "__all__"


class ReplyModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReplyModel
        fields = "__all__"


class ReplyCommentLikeModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReplyCommentLikeModel
        fields = "__all__"


class ViewModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = ViewModel
        fields = "__all__"


class NotificationModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = NotificationModel
        fields = "__all__"
