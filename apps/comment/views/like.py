from rest_framework import viewsets, mixins
from apps.comment.models import LikeComment
from apps.comment.serializers import LikeCommentSerializer

class LikeCommentViewSet(viewsets.ModelViewSet):
	queryset = LikeComment.objects.all()
	serializer_class = LikeCommentSerializer