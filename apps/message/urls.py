from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.message.views import NewMessageViewset, RetrieveMessageViewset

router = DefaultRouter()

router.register(r'', NewMessageViewset, basename='messages')
router.register(r'', RetrieveMessageViewset, basename='messages')

urlpatterns = [
	path('api/messages/', include(router.urls), name='message-routes'),
]