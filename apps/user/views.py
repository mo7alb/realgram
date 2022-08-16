from .models import Profile
from .serializers import ProfileSerializer
from django.contrib.auth import authenticate
from rest_framework.permissions import AllowAny
from rest_framework import generics
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.authtoken.models import Token
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED, HTTP_200_OK
from rest_framework.response import Response

class NewProfile(generics.CreateAPIView):
	queryset = Profile.objects.all()
	serializer_class = ProfileSerializer
	permission_classes = [AllowAny]

class AuthViewSet(viewsets.ViewSet):
    queryset = Profile.objects.all()

    @action(
        detail=False, 
        methods=['post'], 
        name='authenticate users', 
        permission_classes=[AllowAny]
    )
    def authenticate(self, request):
        ''' 
        returns a token which is to be used in the header 

        example 
        login returns token 123

        requesting another api url, include token 123 inside the header as below
        Authorization Token 123
        
        '''
        username = request.data['username']
        password = request.data['password']

        user = authenticate(username=username, password=password)

        if not user:
            return Response(
                {'message': 'invalid credentials'}, 
                status=HTTP_400_BAD_REQUEST
            )

        token, _ = Token.objects.get_or_create(user=user)

        return Response({ 'token': token.key }, status=HTTP_200_OK)

    @action(
        detail=False,
        methods=['post'],
        name='logout'
    )
    def logout(self, request):
        print(request.user.auth_token.delete())
        return Response({ 'message': 'logged out successfully' })