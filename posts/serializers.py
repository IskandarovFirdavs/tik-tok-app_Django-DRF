from rest_framework import serializers
from posts.models import (
    PostModel,
    HashtagModel,
    MusicModel,
    LikeModel,
    CommentModel,
    CommentLikeModel,
    CommentDislikeModel,
    ReplyModel,
    ReplyCommentLikeModel,
    ReplyCommentDislikeModel,
    ViewModel,
    NotificationModel,
)
from users.serializers import UserSerializer, UserModelSerializer, FollowSerializer


# ============================
# 🔹 HASHTAG & MUSIC SERIALIZERS
# ============================

class HashtagModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = HashtagModel
        fields = "__all__"


class MusicModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = MusicModel
        exclude = ("created_at",)


# ============================
# 🔹 COMMENT SERIALIZERS
# ============================

class CommentModelSerializer(serializers.ModelSerializer):
    user = UserModelSerializer(read_only=True)

    class Meta:
        model = CommentModel
        fields = ['id', 'user', 'text', 'created_at']
        read_only_fields = ['id', 'user', 'created_at']


class CommentLikeSerializer(serializers.ModelSerializer):
    user = UserModelSerializer(read_only=True)

    class Meta:
        model = CommentLikeModel
        fields = "__all__"


class CommentDislikeSerializer(serializers.ModelSerializer):
    user = UserModelSerializer(read_only=True)

    class Meta:
        model = CommentDislikeModel
        fields = "__all__"


# ============================
# 🔹 POST SERIALIZER
# ============================

class PostModelSerializer(serializers.ModelSerializer):
    user = UserModelSerializer(read_only=True)
    music = MusicModelSerializer(read_only=True)
    comments = CommentModelSerializer(many=True, read_only=True)
    likes_count = serializers.IntegerField(source='likes.count', read_only=True)
    liked_by_current_user = serializers.SerializerMethodField()
    
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

    def get_liked_by_current_user(self, obj):
        request = self.context.get('request', None)
        if request and request.user.is_authenticated:
            return obj.likes.filter(user=request.user).exists()
        return False

    class Meta:
        model = PostModel
        fields = "__all__"
        



# ============================
# 🔹 LIKE SERIALIZER
# ============================

class LikeModelSerializer(serializers.ModelSerializer):
    user = UserModelSerializer(read_only=True)
    post = PostModelSerializer(read_only=True)

    class Meta:
        model = LikeModel
        fields = ['id', 'user', 'post', 'created_at']
        read_only_fields = ['id', 'user', 'created_at']


# ============================
# 🔹 REPLY & REPLY COMMENT SERIALIZERS
# ============================

class ReplyModelSerializer(serializers.ModelSerializer):
    user = UserModelSerializer(read_only=True)
    post = PostModelSerializer(read_only=True)
    comment = CommentModelSerializer(read_only=True)

    class Meta:
        model = ReplyModel
        fields = "__all__"


class ReplyCommentLikeModelSerializer(serializers.ModelSerializer):
    user = UserModelSerializer(read_only=True)

    class Meta:
        model = ReplyCommentLikeModel
        fields = "__all__"


class ReplyCommentDislikeModelSerializer(serializers.ModelSerializer):
    user = UserModelSerializer(read_only=True)

    class Meta:
        model = ReplyCommentDislikeModel
        fields = "__all__"


# ============================
# 🔹 VIEW & NOTIFICATION SERIALIZERS
# ============================

class ViewModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = ViewModel
        fields = "__all__"



