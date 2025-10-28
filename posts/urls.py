from rest_framework.routers import DefaultRouter
from posts import views

router = DefaultRouter()
router.register(r'genres', views.GenreListViewSet, basename='genres')
router.register(r'likes', views.LikeViewSet, basename='likes')
router.register(r'hashtags', views.HashtagListView, basename='hashtags')
router.register(r'musics', views.MusicListView, basename='musics')
router.register(r'comment_likes', views.CommentLikeViewSet, basename='comment_likes')
router.register(r'comment_dislikes', views.CommentDislikeViewSet, basename='comment_dislikes')
router.register(r'comments', views.CommentView, basename='comments')
router.register(r'reply_comments', views.ReplyCommentView, basename='reply_comments')
router.register(r'reply_comment_likes', views.ReplyCommentLikeView, basename='reply_comment_likes')
router.register(r'reply_comment_dislikes', views.ReplyCommentDislikeView, basename='reply_comment_dislikes')
router.register(r'', views.PostViewSet, basename='posts')

urlpatterns = router.urls
