from datetime import date
from typing import Sequence

from apps.message.models import Message
from apps.message.serializers import MessageSerializer
from apps.user.models import Profile
from django.shortcuts import get_object_or_404
from rest_framework import mixins, status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


class NewMessageViewset(viewsets.GenericViewSet, mixins.CreateModelMixin):
	''' viewset for creating a new message '''
	queryset = Message.objects.all()
	serializer_class = MessageSerializer

	def create(self, request):
		''' create a new message '''
		request_data = request.data

		if 'reciever' not in request_data or 'message' not in request_data:
			return Response(
				{ 'error': 'reciever and message fields are required' }, 
				status=status.HTTP_400_BAD_REQUEST
			)
		
		profile_queryset = Profile.objects.all()
		sender = get_object_or_404(profile_queryset, user=request.user)
		reciever = get_object_or_404(profile_queryset, id=request_data['reciever'])

		try: 
			message = Message(sender=sender, reciever=reciever, message=request_data['message'])
			message.save()

			return Response(status=status.HTTP_201_CREATED)
		except:
			return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)