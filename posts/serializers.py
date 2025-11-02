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
    NotificationModel, SaveModel, RepostModel,
)
from users.serializers import  UserModelSerializer


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
# ============================
# 🔹 COMMENT SERIALIZERS
# ============================
class CommentModelSerializer(serializers.ModelSerializer):
    user = UserModelSerializer(read_only=True)
    replies = serializers.SerializerMethodField()

    likes_count = serializers.SerializerMethodField()
    dislikes_count = serializers.SerializerMethodField()
    liked_by_current_user = serializers.SerializerMethodField()
    disliked_by_current_user = serializers.SerializerMethodField()

    class Meta:
        model = CommentModel
        # hozir barcha kerakli maydonlar
        fields = [
            "id",
            "user",
            "text",
            "created_at",
            "replies",
            "likes_count",
            "dislikes_count",
            "liked_by_current_user",
            "disliked_by_current_user",
        ]
        read_only_fields = ["id", "user", "created_at"]

    def get_replies(self, obj):
        from posts.serializers import ReplyModelSerializer
        replies = obj.replies.all().order_by("created_at")
        return ReplyModelSerializer(replies, many=True, context=self.context).data

    def get_likes_count(self, obj):
        # CommentLikeModel import topida mavjud
        return CommentLikeModel.objects.filter(comment=obj).count()

    def get_dislikes_count(self, obj):
        return CommentDislikeModel.objects.filter(comment=obj).count()

    def get_liked_by_current_user(self, obj):
        request = self.context.get("request", None)
        if request and request.user and request.user.is_authenticated:
            return CommentLikeModel.objects.filter(comment=obj, user=request.user).exists()
        return False

    def get_disliked_by_current_user(self, obj):
        request = self.context.get("request", None)
        if request and request.user and request.user.is_authenticated:
            return CommentDislikeModel.objects.filter(comment=obj, user=request.user).exists()
        return False


# ============================
# 🔹 REPLY SERIALIZER
# ============================
class ReplyModelSerializer(serializers.ModelSerializer):
    user = UserModelSerializer(read_only=True)

    # 🔹 Dynamic fields
    likes_count = serializers.SerializerMethodField()
    dislikes_count = serializers.SerializerMethodField()
    liked_by_current_user = serializers.SerializerMethodField()
    disliked_by_current_user = serializers.SerializerMethodField()

    class Meta:
        model = ReplyModel
        fields = [
            'id',
            'user',
            'post',
            'comment',
            'text',
            'created_at',
            'likes_count',
            'dislikes_count',
            'liked_by_current_user',
            'disliked_by_current_user',
        ]
        read_only_fields = ['id', 'user', 'created_at']

    def get_likes_count(self, obj):
        return ReplyCommentLikeModel.objects.filter(reply_comment=obj).count()

    def get_dislikes_count(self, obj):
        return ReplyCommentDislikeModel.objects.filter(reply_comment=obj).count()

    def get_liked_by_current_user(self, obj):
        request = self.context.get('request', None)
        if request and request.user.is_authenticated:
            return ReplyCommentLikeModel.objects.filter(
                reply_comment=obj, user=request.user
            ).exists()
        return False

    def get_disliked_by_current_user(self, obj):
        request = self.context.get('request', None)
        if request and request.user.is_authenticated:
            return ReplyCommentDislikeModel.objects.filter(
                reply_comment=obj, user=request.user
            ).exists()
        return False


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
    saves_count = serializers.IntegerField(source='saves.count', read_only=True)
    saved_by_current_user = serializers.SerializerMethodField()
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
    reposts_count = serializers.IntegerField(source='reposts.count', read_only=True)
    reposted_by_current_user = serializers.SerializerMethodField()


    def get_liked_by_current_user(self, obj):
        request = self.context.get('request', None)
        if request and request.user.is_authenticated:
            return obj.likes.filter(user=request.user).exists()
        return False

    def get_reposted_by_current_user(self, obj):
        request = self.context.get('request', None)
        if request and request.user.is_authenticated:
            return obj.reposts.filter(user=request.user).exists()
        return False

    def get_saved_by_current_user(self, obj):
        request = self.context.get('request', None)
        if request and request.user.is_authenticated:
            return obj.saves.filter(user=request.user).exists()
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




class SaveModelSerializer(serializers.ModelSerializer):
    user = UserModelSerializer(read_only=True)
    post = PostModelSerializer(read_only=True)

    class Meta:
        model = SaveModel
        fields = ['id', 'user', 'post', 'created_at']
        read_only_fields = ['id', 'user', 'created_at']


class RepostModelSerializer(serializers.ModelSerializer):
    user = UserModelSerializer(read_only=True)
    post_title = serializers.CharField(source='post.title', read_only=True)

    class Meta:
        model = RepostModel
        fields = [
            'id',
            'user',
            'post',
            'post_title',
            'text',
            'created_at'
        ]
        read_only_fields = ['id', 'user', 'created_at']