from typing import Sequence
from django.shortcuts import get_object_or_404
from rest_framework import mixins, viewsets
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from apps.post.models import Post
from apps.user.models import Profile
from apps.post.serializers import PostListSerializer, PostSerializer
from apps.post.tasks import make_post_img
from datetime import date

class PostViewSet(
	mixins.CreateModelMixin,
	mixins.ListModelMixin,
	mixins.RetrieveModelMixin,
	mixins.UpdateModelMixin,
	mixins.DestroyModelMixin,
	viewsets.GenericViewSet
):
	''' 
	Viewset to create, retrieve, update, delete and to get a list of posts 
	'''
	queryset = Post.objects.all()
	serializer_class = PostListSerializer
	permission_classes = [IsAuthenticated]

	def list(self, request) -> Response:
		''' Send a list of posts to the client '''
		# list of all posts
		posts: Sequence[Post] = Post.objects.all().order_by('-created_at')
		# serialize the posts list
		serializer: PostListSerializer = PostListSerializer(posts, many=True)
		# respond to the client with the list
		return Response(serializer.data, status=status.HTTP_200_OK)

	def retrieve(self, request, pk=None) -> Response:
		''' Send a single post to the client '''
		# use shortcut method to find post or to return with a 404 error
		post = get_object_or_404(Post.objects.all(), pk=pk)
		# serialize the post data
		serializer = PostSerializer(post)
		# send the serialized data to the client
		return Response(serializer.data, status=status.HTTP_200_OK)

	def create(self, request) -> Response:
		''' Allow clients to create a new post '''
		data = request.data
		print(data)
		if data["title"] == "":
			return Response({'detail': 'Title is required'}, status=status.HTTP_400_BAD_REQUEST)

		profile = get_object_or_404(Profile.objects.all(), user=request.user)

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

			return Response(status=status.HTTP_201_CREATED)
		except:
			return Response({ 'details': 'Some error occured' }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

	def update(self, request, pk=None):
		''' update a post in the db '''
		request_data = request.data
		if not bool(request_data):
			return Response({ 'details': 'invalid update data' }, status=status.HTTP_400_BAD_REQUEST)

		if 'profile' in request_data:
			return Response({ 'details': 'profile cannot be updated' }, status=status.HTTP_400_BAD_REQUEST)

		# get the post from db
		post = get_object_or_404(Post.objects.all(), pk=pk)
		try:
			# update post 
			Post.objects.filter(pk=pk).update(
				body=request_data['body'] if 'body' in request_data else post.body,
				title=request_data['title'] if 'title' in request_data else post.title,
				caption=request_data['caption'] if 'caption' in request_data else post.caption,
				img=request_data['img'] if 'img' in request_data else post.img,
				updated_at=date.today(),
			)

			# if image is update, rescale the image
			if 'img' in request_data:
				make_post_img(post.pk)
			
			# get the updated post from the db
			post.refresh_from_db()
			# serialize the post 
			serializer = self.get_serializer(post)
			# Respond with an updated post and 202 status code 
			return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
		except:
			# otherwise return with a status code of 500
			return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
