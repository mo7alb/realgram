from rest_framework import serializers
from apps.user.models import Profile
from .models import Comment, LikeComment

class CommentProfileSerializer(serializers.ModelSerializer):
	class Meta: 
		model = Profile
		fields = ['pk']

class CommentSerializer(serializers.ModelSerializer):
	profile = CommentProfileSerializer()
	
	class Meta: 
		model = Comment
		fields = ['pk', 'message', 'profile']

class LikeCommentSerializer(serializers.ModelSerializer):
	class Meta: 
		model = LikeComment
		fields = '__all__'
	