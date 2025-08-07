from django.shortcuts import render
from drf_spectacular.utils import extend_schema, extend_schema_view
from drf_spectacular.utils import OpenApiParameter
from drf_spectacular.utils import OpenApiResponse
from drf_spectacular.utils import OpenApiExample
from drf_spectacular.utils import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter



from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db import transaction
from django.db.models import F
from .models import BlogPost, SubPost, Like
from .serializers import BlogPostSerializer, SubPostSerializer, LikeSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView




@extend_schema_view(
    list=extend_schema(
        summary="Список постов",
        description="Получение списка всех постов с вложенными под-постами, лайками и просмотрами.",
        responses={
            200: OpenApiResponse(
                response=BlogPostSerializer(many=True),
                description="Успешный ответ со списком постов."
            )
        }
    ),
    retrieve=extend_schema(
        summary="Получение поста",
        description="Получение информации о конкретном посте по ID.",
        parameters=[
            OpenApiParameter(name='id', type=int, description='ID поста'),
        ],
        responses={
            200: OpenApiResponse(
                response=BlogPostSerializer,
                description="Успешный ответ с данными поста."
            ),
            404: OpenApiResponse(description="Пост не найден.")
        }
    ),
    create=extend_schema(
        summary='Создание поста',
        description='Создание нового поста с возможностью добавления под-постов.',
        responses={
            201: OpenApiResponse(
                response=BlogPostSerializer,
                description="Пост успешно создан."
            ),
            400: OpenApiResponse(description="Некорректные данные.")
        }
    ),
    update=extend_schema(
        summary='Обновление поста',
        description='Обновление поста и вложенных под-постов атомарно.',
        responses={
            200: OpenApiResponse(
                response=BlogPostSerializer,
                description="Пост успешно обновлен."
            ),
            400: OpenApiResponse(description="Ошибка валидации.")
        }
    ),
    destroy=extend_schema(
        summary='Удаление поста',
        description='Удаление поста по ID.',
        responses={
            204: OpenApiResponse(description="Пост успешно удалён."),
            404: OpenApiResponse(description="Пост не найден.")
        }
    )
)

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
    
@extend_schema_view(
    list=extend_schema(
        summary="Список под-постов",
        description="Получение списка всех под-постов.",
        responses={
            200: OpenApiResponse(
                response=SubPostSerializer(many=True),
                description="Успешный ответ со списком под-постов."
            )
        }
    ),
    retrieve=extend_schema(
        summary="Получение под-поста",
        description="Получение информации о конкретном под-посте по ID.",
        parameters=[
            OpenApiParameter(name='id', type=int, description='ID под-поста'),
        ],
        responses={
            200: OpenApiResponse(
                response=SubPostSerializer,
                description="Успешный ответ с данными под-поста."
            ),
            404: OpenApiResponse(description="Под-пост не найден.")
        }
    ),


    create=extend_schema(
        summary='Создание под-поста',
        description='Создание нового под-поста.',
        responses={
            201: OpenApiResponse(
                response=SubPostSerializer,
                description="Под-пост успешно создан."
            ),
            400: OpenApiResponse(description="Некорректные данные.")
        }
    ),
    update=extend_schema(
        summary='Обновление под-поста',
        description='Обновление под-поста.',
        responses={
            200: OpenApiResponse(
                response=SubPostSerializer,
                description="Под-пост успешно обновлен."
            ),
            400: OpenApiResponse(description="Ошибка валидации.")
        }
    ),



    destroy=extend_schema(
        summary='Удаление под-поста',
        description='Удаление под-поста по ID.',
        responses={
            204: OpenApiResponse(description="Под-пост успешно удалён."),
            404: OpenApiResponse(description="Под-пост не найден.")
        }
    )
    
    
)

class SubPostViewSet(viewsets.ModelViewSet):
    queryset = SubPost.objects.all()
    serializer_class = SubPostSerializer

    

@extend_schema_view(
    list=extend_schema(
        summary="Список лайков",
        description="Получение списка всех лайков.",
        responses={
            200: OpenApiResponse(
                response=LikeSerializer(many=True),
                description="Успешный ответ со списком лайков."
            )
        }
    ),
    retrieve=extend_schema(
        summary="Получение лайка",
        description="Получение информации о конкретном лайке по ID.",
        parameters=[
            OpenApiParameter(name='id', type=int, description='ID лайка'),
        ],
        responses={
            200: OpenApiResponse(
                response=LikeSerializer,
                description="Успешный ответ с данными лайка."
            ),
            404: OpenApiResponse(description="Лайк не найден.")
        }
    ),


    create=extend_schema(
        summary='Создание лайка',
        description='Создание нового лайка.',
        responses={
            201: OpenApiResponse(
                response=LikeSerializer,
                description="Лайк успешно создан."
            ),
            400: OpenApiResponse(description="Некорректные данные.")
        }
    )
)

class LikeViewSet(viewsets.ModelViewSet):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
