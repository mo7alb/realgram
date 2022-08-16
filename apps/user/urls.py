from django.urls import path, include
from .views import NewProfile, AuthViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('', AuthViewSet)

urlpatterns = [
	path('api/profile/register/', NewProfile.as_view()),
	path('api/profile/', include(router.urls))
]