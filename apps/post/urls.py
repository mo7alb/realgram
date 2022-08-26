from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PostViewSet, LikePostViewSet

router = DefaultRouter()
router.register(r'posts', PostViewSet, basename='post-list')
# router.register(r'posts', PostViewSet.create, basename='create-post')
# router.register(r'posts/{pk}', PostViewSet.retrieve, basename='get-post')
# router.register(r'posts/{pk}', PostViewSet.update, basename='update-post')
# router.register(r'posts/{pk}', PostViewSet.destroy, basename='delete-post')
router.register(r'like-post', LikePostViewSet, basename='like-post')

urlpatterns = [
	path('api/', include(router.urls))
]