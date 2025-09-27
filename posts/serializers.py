from rest_framework import serializers
from posts.models import PostModel, HashtagModel, MusicModel


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



class HashtagModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = HashtagModel
        fields = "__all__"


class MusicModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = MusicModel
        fields = "__all__"

