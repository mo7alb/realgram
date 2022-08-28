
from django.shortcuts import get_object_or_404
from rest_framework.permissions import AllowAny
from rest_framework import viewsets, mixins
from rest_framework import status
from rest_framework.response import Response
from apps.comment.models import Comment, LikeComment
from apps.comment.serializers import LikeCommentSerializer
from apps.user.models import Profile

class LikeCommentViewSet(
	mixins.CreateModelMixin,
	mixins.DestroyModelMixin,
	viewsets.GenericViewSet
):
	queryset = LikeComment.objects.all()
	serializer_class = LikeCommentSerializer
	permission_classes = [AllowAny]

	def create(self, request):
		if 'profile' not in request.data or 'comment' not in request.data:
			return Response({'details': 'comment and profile are required'}, status=status.HTTP_400_BAD_REQUEST)

		comment = get_object_or_404(Comment.objects.all(), pk=request.data['comment'])
		profile = get_object_or_404(Profile.objects.all(), id=request.data['profile'])

		likes = LikeComment.objects.filter(comment=comment).filter(profile=profile)

		if len(likes) > 0:
			return Response({ 'details': 'Like already exists' }, status=status.HTTP_400_BAD_REQUEST)

		try: 
			like = LikeComment(
				comment=comment,
				profile=profile
			)
			like.save()
			return Response({ 'details': 'Like created successfully' }, status=status.HTTP_201_CREATED)
		except:
			return Response(
				{ 'details': 'An error occurred while creating the like' }, 
				status=status.HTTP_201_CREATED
			)