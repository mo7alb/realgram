from webbrowser import get
from apps.post.models import LikePost, Post
from apps.post.serializers import LikePostSerializer, LikeSerializer
from apps.user.models import Profile
from django.shortcuts import get_object_or_404, get_list_or_404
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

class LikePostViewSet(
	mixins.CreateModelMixin, 
	mixins.DestroyModelMixin,
	mixins.RetrieveModelMixin,
	viewsets.GenericViewSet
):
	''' viewset to create likes, retrieve them and to destroy them '''
	queryset = LikePost.objects.all()
	serializer_class = LikePostSerializer
	# to be changed (AllowAny is to be replaced with IsAuthenticated)
	permission_classes = [AllowAny]

	def create(self, request) -> Response:
		if 'profile' not in request.data or 'post' not in request.data:
			return Response({'details': 'post and profile are required'}, status=status.HTTP_400_BAD_REQUEST)
		
		post = get_object_or_404(Post.objects.all(), pk=request.data['post'])
		profile = get_object_or_404(Profile.objects.all(), pk=request.data['profile'])

		previous_likes = LikePost.objects.filter(post=post).filter(profile=profile)
		if len(previous_likes) > 0:
			return Response(
				{ 'details': 'like already exists' }, 
				status=status.HTTP_400_BAD_REQUEST
			)
		
		try: 
			like = LikePost(
				post=post,
				profile=profile
			)
			like.save()
			return Response({ 'details': str(like) }, status=status.HTTP_201_CREATED)
		except:
			return Response(
				{ 'details': 'Error creating like' }, 
				status=status.HTTP_500_INTERNAL_SERVER_ERROR
			)

	def destroy(self, request, pk=None) -> Response:
		like = get_object_or_404(LikePost.objects.all(), pk=pk)
		try:
			like.delete()
			return Response(
				{ 'details': 'successfully deleted like' },
				status=status.HTTP_202_ACCEPTED
			)
		except:
			return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

	def retrieve(self, request, pk=None):
		post = get_object_or_404(Post.objects.all(), pk=pk)
		likes = get_list_or_404(LikePost.objects.all(), post=post)

		serializer = LikeSerializer(likes, many=True)

		return Response(serializer.data, status=status.HTTP_200_OK)
