from typing import Sequence

from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from apps.post.models import LikePost, Post
from apps.post.serializers import LikePostSerializer, PostSerializer, PostListSerializer


class PostViewSet(viewsets.ModelViewSet):
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
		all_posts: Sequence[Post] = Post.objects.all()
		# use shortcut method to find post or to return with a 404 error
		post: Post = get_object_or_404(all_posts, pk)

		# serialize the post data
		serializer: PostSerializer = PostSerializer(post)
		# send the serialized data to the client
		return Response(serializer.data, status=status.HTTP_200_OK)

	def create(self, request) -> Response:
		''' Allow clients to create a new post '''
		pass

class LikePostViewSet(viewsets.ModelViewSet):
	queryset = LikePost.objects.all()
	serializer_class = LikePostSerializer
