from .models import Comment, LikeComment
from .serializers import CommentSerializer, LikeCommentSerializer
from rest_framework import viewsets

class CommentViewSet(viewsets.ModelViewSet):
	queryset = Comment.objects.all()
	serializer_class = CommentSerializer

class LikeCommentViewSet(viewsets.ModelViewSet):
	queryset = LikeComment.objects.all()
	serializer_class = LikeCommentSerializer