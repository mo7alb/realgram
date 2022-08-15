from rest_framework import serializers
from apps.user.serializers import ProfileSerializer 
from .models import Comment, LikeComment

class CommentSerializer(serializers.ModelSerializer):
	user = ProfileSerializer()
	
	class Meta: 
		model = Comment
		fields = '__all__'

class LikeCommentSerializer(serializers.ModelSerializer):
	user = ProfileSerializer()
	comment = CommentSerializer()

	class Meta: 
		model = LikeComment
		fields = '__all__'
	