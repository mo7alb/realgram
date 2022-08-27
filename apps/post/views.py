from os import stat
from typing import Sequence

from django.forms.models import model_to_dict
from django.shortcuts import get_object_or_404
from rest_framework import mixins, status, viewsets
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from apps.post.models import LikePost, Post
from apps.post.serializers import (LikePostSerializer, PostListSerializer,
                                   PostSerializer)
from apps.post.tasks import make_post_img
from apps.user.models import Profile


class PostViewSet(
	mixins.CreateModelMixin,
	mixins.ListModelMixin,
	mixins.RetrieveModelMixin,
	viewsets.GenericViewSet
):
	''' 
	Viewset to create, retrieve, update, delete and to get a list of posts 
	'''
	queryset = Post.objects.all()
	serializer_class = PostListSerializer
	permission_classes = [AllowAny]

	def list(self, request) -> Response:
		''' Send a list of posts to the client '''
		# list of all posts
		posts: Sequence[Post] = Post.objects.all().order_by('created_at')
		# serialize the posts list
		serializer: PostListSerializer = PostListSerializer(posts, many=True)

		# respond to the client with the list
		return Response(serializer.data, status=status.HTTP_200_OK)

	def retrieve(self, request, pk=None) -> Response:
		''' Send a single post to the client '''
		# posts query set 
		queryset = Post.objects.all()

		# use shortcut method to find post or to return with a 404 error
		post = get_object_or_404(queryset, pk=pk)
		# serialize the post data
		serializer = PostSerializer(post)
		# send the serialized data to the client
		return Response(serializer.data, status=status.HTTP_200_OK)

	def create(self, request) -> Response:
		''' Allow clients to create a new post '''
		data = {key: request.data[key] for key in list(request.data.keys())}

		if not 'title' in data or not 'profile' in data:
			return Response({'detail': 'Values missing, title and profile are required'}, status=status.HTTP_400_BAD_REQUEST)

		try:
			profile = Profile.objects.get(pk=data['profile'])
			data['profile'] = profile
		except Profile.DoesNotExist:
			return Response({ 'details': 'User not found' }, status=status.HTTP_404_NOT_FOUND)

		try:
			new_post = Post(
				title=data['title'],
				profile=profile,
				img=data['img'] if 'img' in data else None,
				body=data['body'] if 'body' in data else None,
				caption=data['caption'] if 'caption' in data else None,
				created_at=None,
				updated_at=None,
			)
		
			new_post.save()
			
			if 'img' in data:
				make_post_img(new_post.pk)

			return Response({
				'pk': new_post.pk,
				'title': new_post.title
			}, status=status.HTTP_201_CREATED)
		except:
			return Response({ 'details': 'Some error occured' }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class LikePostViewSet(viewsets.ModelViewSet):
	queryset = LikePost.objects.all()
	serializer_class = LikePostSerializer
