from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.message.views import CreateRoomViewSet, RetrieveRoomViewset

router = DefaultRouter()

router.register(r'room', CreateRoomViewSet)
router.register(r'room', RetrieveRoomViewset)

urlpatterns = [
	path('api/message/', include(router.urls))
]