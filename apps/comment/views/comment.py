from django.shortcuts import get_object_or_404, get_list_or_404
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
	mixins.RetrieveModelMixin,
	mixins.UpdateModelMixin,
	viewsets.GenericViewSet
):
	''' 
	viewset to create, update, retrieve and destroy comments 
	'''
	queryset = Comment.objects.all()
	serializer_class = CommentSerializer
	# to be changed in the future from AllowAny to IsAuthenticated
	permission_classes = [AllowAny]

	def create(self, request) -> Response:
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
	
	def retrieve(self, request, pk=None) -> Response:
		''' 
		retrieve list of comments related to a post 
		
		the primary key passed is used as the primary key of the post
		'''
		post = get_object_or_404(Post.objects.all(), pk=pk)
		comments = get_list_or_404(Comment.objects.all(), post=post.pk)

		serializer = CommentSerializer(comments, many=True)
		return Response(serializer.data, status=status.HTTP_200_OK)

	def update(self, request, pk=None) -> Response:
		request_data = request.data
		if 'message' not in request_data or request_data['message'] == '':
			return Response(
				{ 'details': 'message is required' }, 
				status=status.HTTP_400_BAD_REQUEST
			)
		elif 'profile' in request_data or 'post' in request_data:
			return Response(
				{ 'details': 'profile and post cannot be updated' }, 
				status=status.HTTP_400_BAD_REQUEST
			)
		
		comment = get_object_or_404(self.queryset, pk=pk)
		try:
			comment.message = request_data['message']
			comment.save()
			return Response(
				{ 'details': 'Successfully updated comment message' },
				status=status.HTTP_202_ACCEPTED
			)
		except:
			return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)