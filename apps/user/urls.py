from django.urls import path, include
from .views import AuthViewSet, NewProfileViewSet, ProfileRetreivalViewSet
from rest_framework.routers import DefaultRouter

# instanciate a router
router = DefaultRouter()

# let the router know about the viewsets
router.register('', NewProfileViewSet)
router.register('', AuthViewSet)
router.register('', ProfileRetreivalViewSet)

urlpatterns = [
	path('api/profile/', include(router.urls))
]