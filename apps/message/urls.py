from django.urls import path, include
from rest_framework.routers import DefaultRouter
# from apps.message.views import PostViewSet
from apps.message.views import NewMessageViewset

router = DefaultRouter()

router.register(r'', NewMessageViewset, basename='posts')

urlpatterns = [
	path('api/messages/', include(router.urls), name='message-routes'),
]