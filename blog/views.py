from django.shortcuts import render

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db import transaction
from django.db.models import F
from .models import BlogPost, SubPost, Like
from .serializers import BlogPostSerializer, SubPostSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

class BlogPostViewSet(viewsets.ModelViewSet):
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializer

    @action(detail=False, methods=['post'])
    def bulk_create(self, request):
        with transaction.atomic():
            serializer = self.get_serializer(data=request.data, many=True)
            serializer.is_valid(raise_exception=True)
            self.perform_bulk_create(serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

    def perform_bulk_create(self, serializer):
        BlogPost.objects.bulk_create([BlogPost(**item) for item in serializer.validated_data])

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def like(self, request, pk=None):
        post = self.get_object()
        user = request.user
        like, created = Like.objects.get_or_create(user=user, post=post)
        if not created:
            like.delete()
            return Response({'status': 'unliked'})
        return Response({'status': 'liked'})

    @action(detail=True, methods=['get'])
    def view(self, request, pk=None):
        post = self.get_object()
        post.views_count = F('views_count') + 1
        post.save()
        post.refresh_from_db()
        return Response({'views_count': post.views_count})

class SubPostViewSet(viewsets.ModelViewSet):
    queryset = SubPost.objects.all()
    serializer_class = SubPostSerializer
