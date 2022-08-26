from typing import Sequence

from django.contrib.auth.models import User
from rest_framework import serializers

from apps.post.models import LikePost, Post
from apps.user.models import Profile


class ProfileUserSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = ['username']

class PostListProfileSerializer(serializers.ModelSerializer):
	''' Serializer to serailize the profile property of the posts in PostListSerializer'''
	user = ProfileUserSerializer()
	
	class Meta:
		model = Profile
		fields: Sequence[str] = ['id', 'user']


class PostListSerializer(serializers.ModelSerializer):
	'''
		modify the serializer class to return the following 
		username 
		profile id 
		post title 
		post image (if exists)
		post caption (if exists)
	'''
	profile = PostListProfileSerializer()

	class Meta:
		model = Post
		fields: Sequence[str] = ['pk', 'profile', 'title', 'caption', 'img']

class ProfileSerializer(serializers.ModelSerializer):
	class Meta:
		model = Profile
		fields = ['id']

class PostSerializer(serializers.ModelSerializer):
	profile = ProfileSerializer()
	
	class Meta:
		model = Post
		fields = '__all__'

	def create(self, validated_data) -> Post:
		username = list(validated_data.pop('user').values())[0]
		print(username)
		post = Post.objects.create(**validated_data)
		print("post ===> ", post)
		return post

class LikePostSerializer(serializers.ModelSerializer):
	user = ProfileSerializer()
	post = PostSerializer()
	
	class Meta:
		model = LikePost
		fields = '__all__'
