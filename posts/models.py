from django.db import models
from users.models import UserModel


class Hashtag(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return f"#{self.name}"


class MusicModel(models.Model):
    singer = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    file = models.FileField(upload_to='music/')
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return f"{self.name} - {self.singer}"


class Post(models.Model):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name='posts')
    video = models.FileField(upload_to="videos/")
    description = models.TextField(blank=True)
    music = models.ForeignKey(MusicModel, on_delete=models.SET_NULL, null=True, blank=True, related_name="posts")
    hashtags = models.ManyToManyField(Hashtag, blank=True, related_name="posts")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.description[:20]}"


class PostImages(models.Model):
    images = models.ImageField(upload_to='post_images/')

class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="likes")
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name="likes")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("post", "user")

    def __str__(self):
        return f"{self.user.username} liked {self.post.id}"


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name="comments")
    text = models.CharField(max_length=300)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}: {self.text[:20]}"


class CommentLike(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name="likes")
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name="comment_likes")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("comment", "user")

    def __str__(self):
        return f"{self.user.username} liked comment {self.comment.id}"


class Reply(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name="replies")
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name="replies")
    text = models.CharField(max_length=300)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} replied: {self.text[:20]}"


class View(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="views")
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name="views")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("post", "user")

    def __str__(self):
        return f"{self.user.username} viewed {self.post.id}"


class Notification(models.Model):
    NOTIF_TYPE = (
        ("like", "Like"),
        ("comment", "Comment"),
        ("reply", "Reply"),
        ("follow", "Follow"),
    )

    receiver = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name="notifications")
    sender = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name="sent_notifications")
    notif_type = models.CharField(max_length=20, choices=NOTIF_TYPE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True, blank=True)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, null=True, blank=True)
    reply = models.ForeignKey(Reply, on_delete=models.CASCADE, null=True, blank=True)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notif {self.notif_type} to {self.receiver.username}"
