from rest_framework.routers import DefaultRouter
from .views import BlogPostViewSet, SubPostViewSet
from django.urls import path, include

router = DefaultRouter()
router.register(r'posts', BlogPostViewSet, basename='blogpost')
router.register(r'subposts', SubPostViewSet, basename='subpost')


urlpatterns = [
    path('', include(router.urls)), 
    
    
                                                    
]