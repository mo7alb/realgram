from django.shortcuts import get_object_or_404
from rest_framework import viewsets, mixins
from rest_framework import status
from rest_framework.response import Response
from apps.message.models import Room
from apps.message.serializers import RoomSerializer
from apps.user.models import Profile

class RetrieveRoomViewset(mixins.RetrieveModelMixin, viewsets.GenericViewSet):
	''' retrieve chat room '''
	queryset = Room.objects.all()
	serializer_class = RoomSerializer

	def retrieve(self, request, pk=None):
		auth_profile = Profile.objects.get(user=request.user)
		profile = get_object_or_404(Profile.objects.all(), id=pk)
		
		rooms = Room.objects.filter(first_profile=auth_profile, second_profile=profile) | Room.objects.filter(second_profile=auth_profile, first_profile=profile)		
		
		if len(rooms) == 0:
			return Response({ 'error': 'Room does not exists'}, status=status.HTTP_404_NOT_FOUND)
		
		serializer = self.serializer_class(rooms[0])

		return Response(serializer.data, status=status.HTTP_200_OK)