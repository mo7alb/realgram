from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.followers.views import FollowViewset

router = DefaultRouter()
router.register(r'follow', FollowViewset, basename='follows')

urlpatterns = [
	path('api/', include(router.urls), name='post-routes'),
]