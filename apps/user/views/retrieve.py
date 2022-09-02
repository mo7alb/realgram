from apps.user.models import Profile
from apps.user.serializers import ProfileSerializer
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets, mixins
from rest_framework.response import Response
from apps.user.tasks import make_avatar

class ProfileRetreivalViewSet(
	mixins.RetrieveModelMixin,
	mixins.UpdateModelMixin,
	viewsets.GenericViewSet
):
	''' viewset to retrieve a user profile '''
	queryset = Profile.objects.all()

	def retrieve(self, request, pk=None):
		''' retrieve profile data '''
		requestUser = get_object_or_404(self.queryset, user=request.user)

		profile: Profile = get_object_or_404(self.queryset, id=pk)
		serializer = ProfileSerializer(profile)

		same_profile: bool = requestUser == profile

		return Response({**serializer.data, 'same': same_profile}, status=status.HTTP_200_OK)

	def update(self, request, pk=None):
		''' update profile data '''
		request_data = request.data

		profile = get_object_or_404(self.queryset, id=pk)

		# check if both bio and avatar are not sent throught the request
		if 'bio' not in request_data and 'avatar' not in request_data:
			return Response({ 'error': 'either one of bio or avatar is required to be sent'}, status=status.HTTP_400_BAD_REQUEST)

		try:
			# update profile 
			Profile.objects.filter(id=pk).update(
				bio=request_data['bio'] if 'bio' in request_data else profile.bio,
				avatar=request_data['avatar'] if 'avatar' in request_data else profile.avatar,
			)

			# if avatar is update, rescale the avatar image
			if 'avatar' in request_data:
				make_avatar(profile.id)
			
			# Respond with a 202 status code 
			return Response(status=status.HTTP_202_ACCEPTED)
		except:
			# otherwise return with a status code of 500
			return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
