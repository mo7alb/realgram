from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PostViewSet, LikePostViewSet

router = DefaultRouter()
router.register(r'posts', PostViewSet, basename='posts')
router.register(r'like-post', LikePostViewSet, basename='like-post')

urlpatterns = [
	path('api/', include(router.urls), name='post-routes'),
]