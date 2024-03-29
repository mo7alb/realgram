""" realgram URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.frontend.urls')),
    path('', include('apps.user.urls')),
    path('', include('apps.post.urls')),
    path('', include('apps.comment.urls')),
    path('', include('apps.message.urls')),
    path('', include('apps.followers.urls')),
] + static(
    settings.MEDIA_URL_AVATAR,
    document_root=settings.MEDIA_ROOT_AVATAR
) + static(
    settings.MEDIA_URL_POST_IMG,
    document_root=settings.MEDIA_ROOT_POST_IMG
)
