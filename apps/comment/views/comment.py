from django.shortcuts import get_object_or_404
from rest_framework import viewsets, mixins
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from apps.comment.models import Comment
from apps.post.models import Post
from apps.user.models import Profile
from apps.comment.serializers import CommentSerializer

class CommentViewSet(
	mixins.CreateModelMixin,
	viewsets.GenericViewSet
):
	''' 
	viewset to create, update, retrieve and destroy comments 
	'''
	queryset = Comment.objects.all()
	serializer_class = CommentSerializer
	# to be changed in the future from AllowAny to IsAuthenticated
	permission_classes = [AllowAny]

	def create(self, request):
		''' create a new comment '''
		request_data = request.data
		if (
			'message' not in request_data or 
			'post' not in request_data or 
			'profile' not in request_data
		):
			return Response(
				{ 'details': 'message, post and profile are required' },
				status=status.HTTP_400_BAD_REQUEST
			)
		
		post = get_object_or_404(Post.objects.all(), pk=request_data['post'])
		profile = get_object_or_404(Profile.objects.all(), id=request_data['profile'])

		try:
			comment = Comment(
				message=request_data['message'],
				post=post,
				profile=profile
			)
			comment.save()

			return Response(
				{ 'message': comment.message, 'pk': comment.pk },
				status=status.HTTP_201_CREATED
			)
		except:
			return Response(
				{ 'details': 'An error just occurred' },
				status=status.HTTP_500_INTERNAL_SERVER_ERROR
			)