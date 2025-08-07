from typing import Required
from rest_framework import serializers
from .models import BlogPost, Like, SubPost
from django.db import transaction


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

    @transaction.atomic
    def create(self, validated_data):
        subposts_data = validated_data.pop('subposts', [])
        post = BlogPost.objects.create(**validated_data)
        for sub in subposts_data:
            SubPost.objects.create(post=post, **sub)
        return post

    @transaction.atomic
    def update(self, instance, validated_data):
        subposts_data = validated_data.pop('subposts', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if subposts_data is not None:
            existing_ids = [s['id'] for s in subposts_data if 'id' in s]
            instance.subposts.exclude(id__in=existing_ids).delete()

            for sub_data in subposts_data:
                sub_id = sub_data.get('id')
                if sub_id:
                    sub = SubPost.objects.get(id=sub_id, post=instance)
                    sub.title = sub_data['title']
                    sub.body = sub_data['body']
                    sub.save()
                else:
                    SubPost.objects.create(post=instance, **sub_data)

        return instance