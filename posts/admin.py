from django.contrib import admin
from .models import (
    HashtagModel, MusicModel, PostModel,
    LikeModel, CommentModel, CommentLikeModel, ReplyModel, ViewModel, NotificationModel
)


@admin.register(HashtagModel)
class HashtagAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    ordering = ('name',)


class MusicInline(admin.TabularInline):
    model = MusicModel
    extra = 1
    fields = ('music_name', 'file', 'created_at')




@admin.register(MusicModel)
class MusicModelAdmin(admin.ModelAdmin):
    list_display = ('music_name', 'singer', 'created_at')
    search_fields = ('music_name',)
    list_filter = ('created_at', 'singer')
    ordering = ('-created_at',)
    date_hierarchy = 'created_at'

class LikeInline(admin.TabularInline):
    model = LikeModel
    extra = 0
    readonly_fields = ('user', 'created_at')


class CommentInline(admin.TabularInline):
    model = CommentModel
    extra = 0
    readonly_fields = ('user', 'text', 'created_at')


class ViewInline(admin.TabularInline):
    model = ViewModel
    extra = 0
    readonly_fields = ('user', 'created_at')


@admin.register(PostModel)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'music', 'created_at', 'likes_count', 'comments_count', 'views_count')
    search_fields = ('title', 'description', 'user__username', 'hashtags__name')
    list_filter = ('created_at', 'hashtags', 'music')
    filter_horizontal = ('hashtags',)
    readonly_fields = ('created_at',)
    ordering = ('-created_at',)
    date_hierarchy = 'created_at'
    inlines = [LikeInline, CommentInline, ViewInline]

    def likes_count(self, obj):
        return obj.likes.count()
    likes_count.short_description = 'Likes'

    def comments_count(self, obj):
        return obj.comments.count()
    comments_count.short_description = 'Comments'

    def views_count(self, obj):
        return obj.views.count()
    views_count.short_description = 'Views'


@admin.register(LikeModel)
class LikeAdmin(admin.ModelAdmin):
    list_display = ('user', 'post', 'created_at')
    search_fields = ('user__username', 'post__title')
    list_filter = ('created_at',)
    readonly_fields = ('created_at',)
    ordering = ('-created_at',)


class CommentLikeInline(admin.TabularInline):
    model = CommentLikeModel
    extra = 0
    readonly_fields = ('user', 'created_at')


class ReplyInline(admin.TabularInline):
    model = ReplyModel
    extra = 0
    readonly_fields = ('user', 'text', 'created_at')


@admin.register(CommentModel)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'post', 'text_preview', 'created_at', 'likes_count')
    search_fields = ('user__username', 'post__title', 'text')
    list_filter = ('created_at',)
    readonly_fields = ('created_at',)
    ordering = ('-created_at',)
    inlines = [CommentLikeInline, ReplyInline]

    def text_preview(self, obj):
        return obj.text[:50] + '...' if len(obj.text) > 50 else obj.text
    text_preview.short_description = 'Text Preview'

    def likes_count(self, obj):
        return obj.likes.count()
    likes_count.short_description = 'Likes'


@admin.register(CommentLikeModel)
class CommentLikeAdmin(admin.ModelAdmin):
    list_display = ('user', 'comment', 'created_at')
    search_fields = ('user__username', 'comment__text')
    list_filter = ('created_at',)
    readonly_fields = ('created_at',)
    ordering = ('-created_at',)


@admin.register(ReplyModel)
class ReplyAdmin(admin.ModelAdmin):
    list_display = ('user', 'comment', 'text_preview', 'created_at')
    search_fields = ('user__username', 'comment__text', 'text')
    list_filter = ('created_at',)
    readonly_fields = ('created_at',)
    ordering = ('-created_at',)

    def text_preview(self, obj):
        return obj.text[:50] + '...' if len(obj.text) > 50 else obj.text
    text_preview.short_description = 'Text Preview'


@admin.register(ViewModel)
class ViewAdmin(admin.ModelAdmin):
    list_display = ('user', 'post', 'created_at')
    search_fields = ('user__username', 'post__title')
    list_filter = ('created_at',)
    readonly_fields = ('created_at',)
    ordering = ('-created_at',)


@admin.register(NotificationModel)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('receiver', 'sender', 'notif_type', 'post', 'is_read', 'created_at')
    search_fields = ('receiver__username', 'sender__username', 'notif_type')
    list_filter = ('notif_type', 'is_read', 'created_at')
    readonly_fields = ('created_at',)
    ordering = ('-created_at',)
    date_hierarchy = 'created_at'

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('receiver', 'sender', 'post')
