from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api import CommentViewSet, LikeCommentViewSet

router = DefaultRouter()
router.register(r'comment', CommentViewSet)
router.register(r'like-comment', LikeCommentViewSet)

urlpatterns = [
	path('', include(router.urls))
]