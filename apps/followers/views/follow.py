from apps.followers.models import Follow
from apps.followers.serializers import FollowListSerializer
from apps.user.models import Profile
from django.shortcuts import get_object_or_404
from rest_framework import mixins, status, viewsets
from rest_framework.response import Response


class FollowViewset(
	mixins.CreateModelMixin, 
	mixins.DestroyModelMixin, 
	mixins.RetrieveModelMixin, 
	viewsets.GenericViewSet
):
	''' Viewset to create, retrieve a list of and to destroy follows '''
	queryset = Follow.objects.all()
	
	def create(self, request):
		request_data = request.data

		if 'follow' not in request_data:
			return Response(
				{'detail': 'Profile to follow is required'}, 
				status=status.HTTP_400_BAD_REQUEST
			)
		profile = Profile.objects.all().get(user=request.user)
		follows = get_object_or_404(Profile.objects.all(), id=request_data['follow'])

		# check if user follows send user before
		previos_follow = Follow.objects.filter(profile=profile).filter(follows=follows)
		if len(previos_follow) > 0:
			return Response({'details': 'Follow already exists'}, status=status.HTTP_400_BAD_REQUEST)

		try:	
			new_following = Follow(
				profile=profile,
				follows=follows
			)
			new_following.save()
			return Response(
				{'details': '{} started following {}'.format(profile, follows)}, 
				status=status.HTTP_201_CREATED
			)
		except:
			return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

	def retrieve(self, request, pk=None):
		''' returns a list of profiles followed by a profile '''
		profile = get_object_or_404(Profile.objects.all(), id=pk)

		follow_list = self.queryset.filter(profile=profile)
		serializer = FollowListSerializer(follow_list, many=True)

		return Response(serializer.data, status=status.HTTP_200_OK)
