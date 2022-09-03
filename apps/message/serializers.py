from dataclasses import fields
from typing import Sequence

from rest_framework import serializers

from apps.message.models import Message, Room
from apps.user.models import Profile
from apps.post.serializers import ProfileSerializer

class MessageSerializer(serializers.ModelSerializer):
	''' serializer for the message class that abstracts away some message details '''
	reciever = ProfileSerializer()
	sender = ProfileSerializer()
	
	class Meta:
		model = Message
		fields = ['reciever', 'sender', 'pk', 'message']

class RoomSerializer(serializers.ModelSerializer):

	class Meta:
		model = Room
		fields = ['slug']
