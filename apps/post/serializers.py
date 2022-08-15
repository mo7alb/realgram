from rest_framework import serializers
from .models import Post, LikePost
from apps.user.serializers import ProfileSerializer 

class PostSerializer(serializers.ModelSerializer):
	user = ProfileSerializer()
	
	class Meta:
		model = Post
		fields = '__all__'

class LikePostSerializer(serializers.ModelSerializer):
	user = ProfileSerializer()
	post = PostSerializer()
	
	class Meta:
		model = LikePost
		fields = '__all__'