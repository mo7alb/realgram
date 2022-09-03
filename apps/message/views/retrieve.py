import json

from apps.message.models import Message
from apps.message.serializers import MessageSerializer
from apps.user.models import Profile
from django.shortcuts import get_object_or_404
from django.http import QueryDict
from rest_framework import mixins, status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


class RetrieveMessageViewset(mixins.RetrieveModelMixin, viewsets.GenericViewSet):
	''' viewset for creating a new message '''
	queryset = Message.objects.all()
	serializer_class = MessageSerializer

	def retrieve(self, request, pk=None) -> Response:
		''' 
		returns a list of message send or recieved by the user logged in and the user send  
		
		here pk is used to fetch a user profile the user logged in tries to communciate with
		'''
		profile_queryset = Profile.objects.all()

		profile_logged_in = get_object_or_404(profile_queryset, user=request.user)
		profile = get_object_or_404(profile_queryset, id=pk)

		query_1 = self.queryset.filter(sender=profile_logged_in).filter(reciever=profile)
		query_2 = self.queryset.filter(reciever=profile_logged_in).filter(sender=profile)

		serializer = self.serializer_class(query_1 | query_2, many=True)

		return Response(serializer.data ,status=status.HTTP_200_OK)