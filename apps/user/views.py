from rest_framework import generics
from rest_framework.permissions import AllowAny
from .serializers import ProfileSerializer
from .models import Profile

class NewProfile(generics.CreateAPIView):
	queryset = Profile.objects.all()
	serializer_class = ProfileSerializer
	permission_classes = [AllowAny]