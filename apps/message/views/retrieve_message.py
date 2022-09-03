from django.shortcuts import get_object_or_404
from rest_framework import viewsets, mixins
from rest_framework import status
from rest_framework.response import Response
from apps.message.models import Room, Message
from apps.message.serializers import MessageSerializer, RoomSerializer
from apps.user.models import Profile

class RetrieveMessageViewset(mixins.RetrieveModelMixin, viewsets.GenericViewSet):
	''' retrieve chat room '''
	queryset = Message.objects.all()
	serializer_class = MessageSerializer

	def retrieve(self, request, pk=None):
		room = get_object_or_404(Room.objects.all(), slug=pk)
		messages = self.queryset.filter(room=room)
		
		serializer = self.serializer_class(messages, many=True)

		return Response(serializer.data, status=status.HTTP_200_OK)