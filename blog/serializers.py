from typing import Required
from rest_framework import serializers
from .models import BlogPost, Like, SubPost

class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ['id', 'user', 'post']

    def create(self, validated_data):
        return Like.objects.create(**validated_data)
        # Здесь можно добавить логику для создания лайка, если нужно
        


class SubPostSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)

    class Meta:
        model = SubPost
        fields = ['id', 'title', 'body']

class BlogPostSerializer(serializers.ModelSerializer):
    subposts = SubPostSerializer(many=True, required=False)
    likes_count = serializers.IntegerField(source='likes.count', read_only=True)

    class Meta:
        model = BlogPost
        fields = ['id', 'title', 'body', 'author', 'created_at', 'updated_at', 'views_count', 'likes_count', 'subposts']

    