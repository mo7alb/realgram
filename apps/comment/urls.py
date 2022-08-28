from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.comment.views import CommentViewSet, LikeCommentViewSet

router = DefaultRouter()
router.register(r'comments', CommentViewSet)
router.register(r'like-comment', LikeCommentViewSet)

urlpatterns = [
	path('api/', include(router.urls))
]