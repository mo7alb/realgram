from dataclasses import fields
from rest_framework import serializers
from .models import Profile
from django.contrib.auth.models import User
import datetime

class UserSerializer (serializers.ModelSerializer):
	class Meta:
		model = User
		fields = [
			'email',
			'id',
			'username',
			'first_name',
			'last_name',
			'password'
		]
	
	def create(self, validated_data):
		return User.objects.create(**validated_data)

class ProfileSerializer(serializers.ModelSerializer):
	user = UserSerializer()
	
	class Meta:
		model = Profile
		fields = '__all__'

	def create(self, validated_data):
		''' create a profile for the user '''
		bio = validated_data.pop('bio')
		avatar = validated_data.pop('avatar')
		profile = Profile(
			user=validated_data.pop('user'), 
			bio=bio, 
			avatar=avatar
		)
		profile.save()

		return profile


class AuthUserSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = ['username', 'password']

class AuthProfileSerializer(serializers.ModelSerializer):
	user = AuthUserSerializer()
	class Meta:
		model = Profile
		fields = ['user']