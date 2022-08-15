from .models import Post, LikePost
from .serializers import PostSerializer, LikePostSerializer
from rest_framework import viewsets

class PostViewSet(viewsets.ModelViewSet):
	queryset = Post.objects.all()
	serializer_class = PostSerializer

class LikePostViewSet(viewsets.ModelViewSet):
	queryset = LikePost.objects.all()
	serializer_class = LikePostSerializer