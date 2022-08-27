from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate 
from rest_framework import viewsets
from rest_framework import status
from apps.user.models import Profile
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

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
        if (key not in request.data for key in ['username','password']):
            return Response(
					{'error': 'username and password are required'}, 
					status=status.HTTP_400_BAD_REQUEST
				)

        username = request.data['username']
        password = request.data['password']

        user = authenticate(username=username, password=password)

        if not user:
            return Response(
                {'error': 'invalid credentials'}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        token, _ = Token.objects.get_or_create(user=user)

        return Response({ 'token': token.key }, status=status.HTTP_200_OK)

    @action(
        detail=False,
        methods=['post'],
        name='logout',
        permission_classes=[IsAuthenticated]
    )
    def logout(self, request):
        request.user.auth_token.delete()
        return Response(
            { 'message': 'logged out successfully' }, 
            status=status.HTTP_200_OK
        )
