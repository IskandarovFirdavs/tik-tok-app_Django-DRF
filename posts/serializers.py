from rest_framework import serializers
from posts.models import PostModel, HashtagModel, MusicModel, LikeModel, CommentModel, CommentLikeModel, ReplyModel, \
    ReplyCommentLikeModel, ViewModel, NotificationModel
from users.serializers import UserSerializer, UserModelSerializer


class HashtagModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = HashtagModel
        fields = "__all__"


class MusicModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = MusicModel
        exclude = "created_at",


# posts/serializers.py
class PostModelSerializer(serializers.ModelSerializer):
    user = UserModelSerializer(read_only=True)
    music = MusicModelSerializer(read_only=True)
    music_id = serializers.PrimaryKeyRelatedField(
        queryset=MusicModel.objects.all(),
        write_only=True,
        source="music",
        required=False,
        allow_null=True
    )
    hashtags = HashtagModelSerializer(many=True, read_only=True)
    hashtag_ids = serializers.PrimaryKeyRelatedField(
        queryset=HashtagModel.objects.all(),
        many=True,
        write_only=True,
        source="hashtags",
        required=False
    )

    class Meta:
        model = PostModel
        fields = ["id", "post", "user", "music", "music_id",
                  "hashtags", "hashtag_ids", "title", "description", "created_at"]

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
