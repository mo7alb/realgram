from apps.user.models import Profile
from apps.user.serializers import ProfileSerializer
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.response import Response

class ProfileRetreivalViewSet(viewsets.ViewSet):
	''' viewset to retrieve a user profile '''
	queryset = Profile.objects.all()

	def retrieve(self, request, pk=None):
		profile = get_object_or_404(self.queryset, id=pk)
		serializer = ProfileSerializer(profile)

		return Response(serializer.data, status=status.HTTP_200_OK)
