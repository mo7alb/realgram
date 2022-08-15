from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api import PostViewSet, LikePostViewSet

router = DefaultRouter()
router.register(r'post', PostViewSet)
router.register(r'like-post', LikePostViewSet)

urlpatterns = [
	path('', include(router.urls))
]