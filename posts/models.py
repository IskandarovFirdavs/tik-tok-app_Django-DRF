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
    class GenreChoice(models.TextChoices):
        Singing_dancing = 'SINGING_DANCING', 'Singing_dancing'
        Comedy = 'COMEDY', 'Comedy'
        Sports = 'SPORTS', 'Sports'
        Anime_comics = 'ANIME_COMICS', 'Anime_comics'
        Relationship = 'RELATIONSHIP', 'Relationship'
        Shows = 'SHOWS', 'Shows'
        Daily_life = 'DAILY_LIFE', 'Daily_life'
        Beauty_care = 'BEAUTY_CARE', 'Beauty_care'
        Games = 'GAMES', 'Games'
        Society = 'SOCIETY', 'Society'
        Outfit = 'OUTFIT', 'Outfit'
        Cars = 'CARS', 'Cars'
        Food = 'FOOD', 'Food'
        Animals = 'ANIMALS', 'Animals'
        Family = 'FAMILY', 'Family'
        Drama = 'DRAMA', 'Drama'
        Fitness_health = 'FITNESS_HEALTH', 'Fitness_health'
        Education = 'EDUCATION', 'Education'
        Technology = 'TECHNOLOGY', 'Technology'


    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name='posts')
    post = models.FileField(upload_to="posts/")
    title = models.CharField(max_length=100)
    description = models.CharField(null=True, blank=True, max_length=255)
    music = models.ForeignKey(MusicModel, on_delete=models.SET_NULL, null=True, blank=True, related_name="posts")
    hashtags = models.ManyToManyField(HashtagModel, blank=True, related_name="posts")
    created_at = models.DateTimeField(auto_now_add=True)
    saved = models.BooleanField(default=False)
    genre = models.CharField(max_length=30, choices=GenreChoice, null=True, blank=True)
    saves = models.ManyToManyField(
        UserModel,
        null=True,
        blank=True,
        related_name='saved_posts'
    )
    reposts = models.ManyToManyField(
        UserModel,
        null=True, blank=True,
        related_name='reposts'
    )

    def __str__(self):
        return self.user.username


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


class CommentDislikeModel(models.Model):
    comment = models.ForeignKey(CommentModel, on_delete=models.CASCADE, related_name="dislikes")
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name="comment_dislikes")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("comment", "user",)

    def __str__(self):
        return f"{self.user.username} disliked comment {self.comment.id}"


class ReplyModel(models.Model):
    post = models.ForeignKey(PostModel, on_delete=models.CASCADE, related_name='replies')
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


class ReplyCommentDislikeModel(models.Model):
    reply_comment = models.ForeignKey(ReplyModel, on_delete=models.CASCADE, related_name="reply_dislikes")
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name="reply_comment_dislikes")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("reply_comment", "user")

    def __str__(self):
        return f"{self.user.username} disliked comment {self.reply_comment.id}"


class ViewModel(models.Model):
    post = models.ForeignKey(PostModel, on_delete=models.CASCADE, related_name="views")
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name="views")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("post", "user")

    def __str__(self):
        return f"{self.user.username} viewed {self.post.id}"


class NotificationModel(models.Model):
    class NotifType(models.TextChoices):
        Like = "LIKE", "Like"
        Follow = "FOLLOW", "Follow"
        Comment = "COMMENT", "Comment"
        reply = "REPLY", "reply"

    receiver = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name="notifications")
    sender = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name="sent_notifications")
    notif_type = models.CharField(max_length=20, choices=NotifType)
    post = models.ForeignKey(PostModel, on_delete=models.CASCADE, null=True, blank=True)
    comment = models.ForeignKey(CommentModel, on_delete=models.CASCADE, null=True, blank=True)
    reply = models.ForeignKey(ReplyModel, on_delete=models.CASCADE, null=True, blank=True)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notif {self.notif_type} to {self.receiver.username}"

