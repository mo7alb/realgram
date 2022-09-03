from django.shortcuts import get_object_or_404
from rest_framework import viewsets, mixins
from rest_framework import status
from rest_framework.response import Response
from apps.message.models import Room
from apps.message.serializers import RoomSerializer
from apps.user.models import Profile

class CreateRoomViewSet(
	mixins.CreateModelMixin,
	viewsets.GenericViewSet
):
	''' 
	viewset to create a chatting room
	'''
	queryset = Room.objects.all()
	serializer_class = RoomSerializer

	def create(self, request):
		''' create a new room '''
		request_data = request.data

		if 'profile' not in request_data:
			return Response({ 'details': 'Profile is required'}, status=status.HTTP_400_BAD_REQUEST)

		first_profile = Profile.objects.get(user=request.user)
		second_profile = get_object_or_404(Profile.objects.all(), id=request_data['profile'])

		previous_room = Room.objects.filter(first_profile=first_profile, second_profile=second_profile) | Room.objects.filter(second_profile=first_profile, first_profile=second_profile)
		if len(previous_room) > 0:
			return Response({ 'details': 'Room already exists'}, status=status.HTTP_400_BAD_REQUEST)

		try: 
			new_room = Room(
				slug='{}-{}'.format(first_profile.id, second_profile.id),
				first_profile=first_profile,
				second_profile=second_profile
			)
			new_room.save()

			return Response(status=status.HTTP_201_CREATED)
		except:
			return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)