from rest_framework import serializers
from .models import Profile
from django.contrib.auth.models import User

class UserSerializer (serializers.ModelSerializer):
	class Meta:
		model = User
		fields = [
			'email',
			'id',
			'username',
			'first_name',
			'last_name',
			'password'
		]

class ProfileSerializer(serializers.ModelSerializer):
	user = UserSerializer()
	
	class Meta:
		model = Profile
		fields = '__all__'

	def create(self, validated_data):
		''' create a new user profile '''
		password = validated_data['user'].pop('password')
		username = validated_data['user'].pop('username')
		first_name = validated_data['user'].pop('first_name')
		last_name = validated_data['user'].pop('last_name')
		email = validated_data['user'].pop('email')

		''' create a django auth user first '''
		user = User(
			username=username, 
			email=email, 
			first_name=first_name, 
			last_name=last_name
		)
		user.set_password(password)
		user.save()

		''' create a profile for the user '''
		date_of_birth = validated_data.pop('date_of_birth')
		date_of_birth = str(date_of_birth)

		bio = validated_data.pop('bio')
		avatar = validated_data.pop('avatar')
		profile = Profile(
			user=user, 
			date_of_birth=date_of_birth, 
			bio=bio, 
			avatar=avatar
		)
		profile.save()

		return profile