from django.shortcuts import get_object_or_404, get_list_or_404
from rest_framework.permissions import AllowAny
from rest_framework import viewsets, mixins
from rest_framework import status
from rest_framework.response import Response
from apps.comment.models import Comment, LikeComment
from apps.comment.serializers import LikeCommentSerializer, LikeSerializer
from apps.user.models import Profile

class LikeCommentViewSet(
	mixins.CreateModelMixin,
	mixins.DestroyModelMixin,
	mixins.RetrieveModelMixin,
	viewsets.GenericViewSet
):
	queryset = LikeComment.objects.all()
	serializer_class = LikeCommentSerializer
	permission_classes = [AllowAny]

	def create(self, request):
		''' create a like for a comment '''
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
			return Response(
				{ 'details': str(like) }, 
				status=status.HTTP_201_CREATED
			)
		except:
			return Response(
				{ 'details': 'An error occurred while creating the like' }, 
				status=status.HTTP_201_CREATED
			)
	
	def retrieve(self, request, pk=None):
		''' 
		retrieve list of likes on a comment

		here pk is used to fetch a comment
		'''
		comment = get_object_or_404(Comment.objects.all(), pk=pk)
		likes = get_list_or_404(self.queryset, comment=comment)

		serializer = LikeSerializer(likes, many=True)
		return Response(serializer.data, status=status.HTTP_200_OK)
