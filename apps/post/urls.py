from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.post.views import PostViewSet

router = DefaultRouter()

router.register(r'', PostViewSet, basename='posts')

urlpatterns = [
	path('api/posts/', include(router.urls), name='post-routes'),
]