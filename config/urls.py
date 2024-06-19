"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView
from rest_framework.routers import DefaultRouter
from djoser.views import UserViewSet, TokenCreateView
from django.conf import settings
from django.conf.urls.static import static
from api.permission import AllowSignupAndLogin

class CustomUserViewSet(UserViewSet):
    permission_classes = [AllowSignupAndLogin]

class CustomTokenCreateView(TokenCreateView):
    permission_classes = [AllowSignupAndLogin]

# Define your router
router = DefaultRouter()
router.register(r'users', CustomUserViewSet, basename='user')


urlpatterns = [
    # app urls
    path('',include('api.urls')), # core app
    path('api-auth/', include('rest_framework.urls')), # restframework
    # djoser
    path('auth/', include(router.urls)),
    path('auth/token/login/', CustomTokenCreateView.as_view(), name='login'),
    path('auth/', include('djoser.urls.authtoken')), 
    # api docs
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'), # spect for api docs
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    # admin
    path('admin/', admin.site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
