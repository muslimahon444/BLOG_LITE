
from django.contrib import admin
from django.urls import path,include
from rest_framework import routers
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

from drf_spectacular.settings import spectacular_settings



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('blog.urls')),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='docs'), 


]
