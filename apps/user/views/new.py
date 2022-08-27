from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework import status
from apps.user.models import Profile
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from apps.user.tasks import make_avatar

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
		request_data = request.data

		if (key not in request_data for key in [
			'username',
			'email',
			'first_name',
			'last_name',
			'password'
		]):
			return Response(status=status.HTTP_400_BAD_REQUEST)

		usernames = User.objects.filter(username=request_data['username'])
		if len(usernames) > 0:
			return Response({ 'error': 'username already exists' }, status=status.HTTP_400_BAD_REQUEST)
		emails = User.objects.filter(email=request_data['email'])
		if len(emails) > 0:
			return Response({ 'error': 'email already exists' }, status=status.HTTP_400_BAD_REQUEST)

		try:
			# create a user
			user = User(
				username=request_data['username'],
				email=request_data['email'],
				first_name=request_data['first_name'],
				last_name=request_data['last_name']
			)
			# set user password 
			user.set_password(request_data['password'])
			# save user to db
			user.save()

			if 'avatar' in request_data and 'bio' in request_data:
				# create a profile for the user
				profile = Profile(
					user=user,
					bio=request_data['bio'],
					avatar=request_data['avatar']
				)
			
				# save profile to db
				profile.save()
				make_avatar.delay(profile.pk)
			elif 'avatar' not in request_data and 'bio' in request_data:
				profile = Profile(
					user=user,
					bio=request_data['bio'],
				)
				profile.save()
			else :
				profile = Profile(
					user=user
				)
				profile.save()

			# return 201 response as user and profile were successfully created
			return Response(
				{ 
					'profile': {
						'id': profile.pk, 
						'username': user.username,
						'email': user.email,
					}
				}, status=status.HTTP_201_CREATED
			)

		except:
			return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

