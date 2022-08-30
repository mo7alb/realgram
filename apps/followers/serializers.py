from rest_framework import serializers
from apps.followers.models import Follow
from apps.user.models import Profile, User

class UserSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = ['pk', 'username']

class ProfileSerializer(serializers.ModelSerializer):
	user = UserSerializer()

	class Meta:
		model = Profile
		fields = ['id', 'user']

class FollowListSerializer(serializers.ModelSerializer):
	profile = ProfileSerializer()
	follows = ProfileSerializer()

	class Meta:
		model = Follow
		fields = ['pk', 'profile', 'follows']