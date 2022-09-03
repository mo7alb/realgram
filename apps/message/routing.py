from django.urls import re_path

from apps.message.consumer import ChatConsumer

websocket_urlpatterns = [
	re_path(r'ws/(?P<slug>\w+)/$', ChatConsumer) 
]