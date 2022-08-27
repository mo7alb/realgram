from turtle import pos
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, mixins
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from apps.post.models import LikePost, Post
from apps.user.models import Profile
from apps.post.serializers import LikePostSerializer, ProfileSerializer, PostSerializer

class LikePostViewSet(
	mixins.CreateModelMixin, 
	mixins.DestroyModelMixin,
	viewsets.GenericViewSet
):
	''' viewset to create likes, retrieve them and to destroy them '''
	queryset = LikePost.objects.all()
	serializer_class = LikePostSerializer
	# to be changed (AllowAny is to be replaced with IsAuthenticated)
	permission_classes = [AllowAny]

	def create(self, request):
		if 'profile' not in request.data or 'post' not in request.data:
			return Response({'details': 'post and profile are required'}, status=status.HTTP_400_BAD_REQUEST)
		
		post = get_object_or_404(Post.objects.all(), pk=request.data['post'])
		profile = get_object_or_404(Profile.objects.all(), pk=request.data['profile'])

		try:
			previous_likes = LikePost.objects.filter(post=post).filter(profile=profile)
			if len(previous_likes) > 0:
				return Response(
					{ 'details': 'like already exists' }, 
					status=status.HTTP_400_BAD_REQUEST
				)
		except:
			return Response(
				{ 'details': 'Error creating like' }, 
				status=status.HTTP_500_INTERNAL_SERVER_ERROR
			)
		
		try: 
			like = LikePost(
				post=post,
				profile=profile
			)
			like.save()
			return Response({ 'details': str(like) })
		except:
			return Response(
				{ 'details': 'Error creating like' }, 
				status=status.HTTP_500_INTERNAL_SERVER_ERROR
			)
