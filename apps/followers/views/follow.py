from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets, mixins
from rest_framework import status
from rest_framework.response import Response
from apps.followers.models import Follow
from apps.user.models import Profile

class Follow(
	mixins.CreateModelMixin,
	mixins.DestroyModelMixin,
	viewsets.GenericViewSet
):
	''' Viewset to create and destroy follows '''
	queryset = Follow.objects.all()
	permission_classes = [IsAuthenticated]

	def create(self, request):
		''' create a new follow '''
		request_data = request.data

		if 'follows' not in request.data:
			return Response({'details': 'follow profile is required'}, status=status.HTTP_400_BAD_REQUEST)

		profile = Profile.objects.get(user=request.user)
		print(profile)

		follows = get_object_or_404(Profile.objects.all(), pk=request_data['follows'])
		print(follows)

		try:
			new_following = Follow(profile=profile, follows=follows)
			new_following.save()
			return Response(
				{'details': '{} started following {}'.format(profile, follows)}, 
				status=status.HTTP_200_OK
			)
		except:
			return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
			