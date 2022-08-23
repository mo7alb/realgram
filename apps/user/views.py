from .models import Profile
from django.contrib.auth import authenticate 
from django.contrib.auth.models import User
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.authtoken.models import Token
from rest_framework import status
from rest_framework.response import Response
from .tasks import make_avatar

class NewProfileViewSet(viewsets.ViewSet):
    queryset = Profile.objects.all()

    @action(
        detail=False, 
        methods=['post'], 
        name='register users', 
        permission_classes=[AllowAny]
    )
    def register(self, request):
        ''' allows new users to register '''
        data_fields = list(request.data.keys())

        if (
            'username' not in data_fields or 
            'email' not in data_fields or 
            'first_name' not in data_fields or 
            'last_name' not in data_fields or 
            'password' not in data_fields
        ):
            return Response(status=status.HTTP_400_BAD_REQUEST)

        user_data = {
            'username': request.data['username'],
            'email': request.data['email'],
            'first_name': request.data['first_name'],
            'last_name': request.data['last_name'],
            'password': request.data['password'],
        }

        usernames = User.objects.filter(username=user_data['username'])
        if len(usernames) > 0:
            return Response({ 'error': 'username already exists' }, status=status.HTTP_400_BAD_REQUEST)
        emails = User.objects.filter(email=user_data['email'])
        if len(emails) > 0:
            return Response({ 'error': 'email already exists' }, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            # create a user
            user = User(
                username=user_data['username'],
                email=user_data['email'],
                first_name=user_data['first_name'],
                last_name=user_data['last_name']
            )
            # set user password 
            user.set_password(user_data['password'])
            # save user to db
            user.save()

            bio = request.data['bio'] if 'bio' in data_fields else None
            avatar = request.data['avatar'] if 'avatar' in data_fields else None

            # create a profile for the user
            profile = Profile(
                user=user,
                bio=bio,
                avatar=avatar
            )
            # save profile to db
            profile.save()

            if avatar != None:
                make_avatar.delay(profile.pk)

            # return 201 response as user and profile were successfully created
            return Response({ 'profile': {
                'id': profile.pk, 
                'username': user.username,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email,
                'bio': profile.bio,
            } }, status=status.HTTP_201_CREATED)
            
        except:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

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
        data_fields = list(request.data.keys())

        if (
            'username' not in data_fields or 
            'password' not in data_fields 
        ):
            return Response(status=status.HTTP_400_BAD_REQUEST)

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
        return Response({ 'message': 'logged out successfully' })
