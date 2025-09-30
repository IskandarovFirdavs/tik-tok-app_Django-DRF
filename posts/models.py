from django.db import models
from users.models import UserModel


class HashtagModel(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return f"#{self.name}"


class MusicModel(models.Model):
    cover = models.ImageField(upload_to='music/', null=True, blank=True)
    singer = models.CharField(max_length=100)
    music_name = models.CharField(max_length=100, unique=True)
    file = models.FileField(upload_to='music/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.music_name} - {self.singer} "


class PostModel(models.Model):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name='posts')
    post = models.FileField(upload_to="posts/")
    title = models.CharField(max_length=100)
    description = models.CharField(null=True, blank=True, max_length=255)
    music = models.ForeignKey(MusicModel, on_delete=models.SET_NULL, null=True, blank=True, related_name="posts")
    hashtags = models.ManyToManyField(HashtagModel, blank=True, related_name="posts")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.description[:20]}"


class LikeModel(models.Model):
    post = models.ForeignKey(PostModel, on_delete=models.CASCADE, related_name="likes")
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name="likes")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("post", "user")

    def __str__(self):
        return f"{self.user.username} liked {self.post.id}"


class CommentModel(models.Model):
    post = models.ForeignKey(PostModel, on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name="comments")
    text = models.CharField(max_length=300)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}: {self.text[:20]}"


class CommentLikeModel(models.Model):
    comment = models.ForeignKey(CommentModel, on_delete=models.CASCADE, related_name="likes")
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name="comment_likes")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("comment", "user",)

    def __str__(self):
        return f"{self.user.username} liked comment {self.comment.id}"


class ReplyModel(models.Model):
    comment = models.ForeignKey(CommentModel, on_delete=models.CASCADE, related_name="replies")
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name="replies")
    text = models.CharField(max_length=300)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} replied: {self.text[:20]}"


class ReplyCommentLikeModel(models.Model):
    reply_comment = models.ForeignKey(ReplyModel, on_delete=models.CASCADE, related_name="reply_likes")
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name="reply_comment_likes")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("reply_comment", "user")

    def __str__(self):
        return f"{self.user.username} liked comment {self.reply_comment.id}"


class ViewModel(models.Model):
    post = models.ForeignKey(PostModel, on_delete=models.CASCADE, related_name="views")
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name="views")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("post", "user")

    def __str__(self):
        return f"{self.user.username} viewed {self.post.id}"


class NotificationModel(models.Model):
    NOTIF_TYPE = (
        ("like", "Like"),
        ("comment", "Comment"),
        ("reply", "Reply"),
        ("follow", "Follow"),
    )

    receiver = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name="notifications")
    sender = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name="sent_notifications")
    notif_type = models.CharField(max_length=20, choices=NOTIF_TYPE)
    post = models.ForeignKey(PostModel, on_delete=models.CASCADE, null=True, blank=True)
    comment = models.ForeignKey(CommentModel, on_delete=models.CASCADE, null=True, blank=True)
    reply = models.ForeignKey(ReplyModel, on_delete=models.CASCADE, null=True, blank=True)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notif {self.notif_type} to {self.receiver.username}"
