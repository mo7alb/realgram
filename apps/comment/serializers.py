from rest_framework import serializers
from apps.user.models import Profile
from apps.user.serializers import ProfileSerializer
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
	comment = CommentSerializer()
	profile = ProfileSerializer()
	
	class Meta: 
		model = LikeComment
		fields = [
			'comment',
			'profile'
		]
	
class LikeSerializer(serializers.ModelSerializer):
	class Meta: 
		model = LikeComment
		fields = ['id']
	