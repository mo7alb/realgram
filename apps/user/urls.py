from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api import UserViewSet, ProfileViewSet

router = DefaultRouter()
router.register(r'user', UserViewSet) # might not need this
router.register(r'profile', ProfileViewSet)

urlpatterns = [
	path('', include(router.urls))
]