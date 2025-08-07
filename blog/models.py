
from django.db import models
from django.contrib.auth.models import User




class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.CharField(max_length=100)
    body = models.TextField(blank=True,null=True)
    views_count = models.IntegerField(default=0)


class SubPost(models.Model):
    title = models.CharField(max_length=200)  
    body = models.TextField()
    post = models.ForeignKey(BlogPost, related_name='subposts', on_delete=models.CASCADE)


class Like(models.Model):
    post = models.ForeignKey(BlogPost, related_name='likes', on_delete=models.CASCADE)
    user = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('post', 'user')
