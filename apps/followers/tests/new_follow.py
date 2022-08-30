from django.contrib.auth.hashers import make_password
from apps.user.models import Profile, User
from apps.followers.models import Follow
from rest_framework import status
from rest_framework.test import APITestCase

class NewFollowTestCase(APITestCase):
	def setUp(self) -> None:
		''' set up common variables to be used within tests'''
		Profile.objects.create(user=User.objects.create(
			username='doey', 
			email='doey@do.com', 
			first_name='doey', 
			last_name='doey',
			password=make_password('secret')
		))
		follow_profile = Profile.objects.create(
			user=User.objects.create(
				username="johndoe",
				first_name="john",
				last_name="johndoe",
				email="johndoe@somemail.com",
				password=make_password('super secret')
			)
		)
		self.url = '/api/follow/'
		self.data = { 'follow': follow_profile.id }
		# authenticate user and get authorization toke
		token = self.client.post('/api/profile/authenticate/', {'username': 'doey','password': 'secret'}).json()['token']
		# set up header
		self.header = {'HTTP_AUTHORIZATION': 'Token {}'.format(token)}

	def tearDown(self) -> None:
		''' flush database once all tests are done '''
		Follow.objects.all().delete()
		Profile.objects.all().delete()
		User.objects.all().delete()

	def test_new_follow_fails_unauthorized(self):
		''' test if following a user fails with status code of 401 if unauthorized '''
		response = self.client.post(self.url, self.data)
		self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

	def test_new_follow_success_status(self):
		''' test if following a user returns a status code of 201 '''
		response = self.client.post(self.url, self.data, **self.header)
		self.assertEqual(response.status_code, status.HTTP_201_CREATED)

	def test_new_follow_success_message(self):
		''' test if following a user returns a correct message '''
		response = self.client.post(self.url, self.data, **self.header).json()
		self.assertEqual(response['details'], 'doey started following johndoe')
	
	def test_new_follow_invalid_data(self):
		''' test if passing invalid data returns a status code of 400 '''
		response = self.client.post(self.url, {}, **self.header)
		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
	
	def test_new_follow_invalid_profile(self):
		''' test if passing profile to follow returns a status code of 404 '''
		response = self.client.post(self.url, { 'follow': 120 }, **self.header)
		self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
	
	def test_new_follow_twice(self):
		''' test if following a user twice returns a status code of 400 '''

		response = self.client.post(self.url, self.data, **self.header)
		second_response = self.client.post(self.url, self.data, **self.header)
		self.assertEqual(second_response.status_code, status.HTTP_400_BAD_REQUEST)
