from django.contrib.auth.models import User
from .models import Profile
from .serializers import UserSerializer, ProfileSerializer
from rest_framework import viewsets

class UserViewSet(viewsets.ModelViewSet):
	queryset = User.objects.all()
	serializer_class = UserSerializer


class ProfileViewSet(viewsets.ViewSet):
	queryset = Profile.objects.all()
	serializer_class = ProfileSerializer
