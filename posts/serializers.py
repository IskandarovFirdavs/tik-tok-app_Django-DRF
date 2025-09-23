from rest_framework import serializers
from posts.models import PostModel


class PostModelSerializer(serializers.ModelSerializer):
    post = serializers.SerializerMethodField()

    def get_post(self, obj):
        request = self.context.get('request')
        if obj.post and request:
            return request.build_absolute_uri(obj.post.url)
        return obj.post.url if obj.post else None


    class Meta:
        model = PostModel
        fields = "__all__"

