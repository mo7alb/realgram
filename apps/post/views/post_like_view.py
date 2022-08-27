from rest_framework import viewsets, mixins
from apps.post.models import LikePost
from apps.post.serializers import LikePostSerializer

class LikePostViewSet(viewsets.ModelViewSet):
	''' viewset to create likes and to destroy them '''
	queryset = LikePost.objects.all()
	serializer_class = LikePostSerializer
