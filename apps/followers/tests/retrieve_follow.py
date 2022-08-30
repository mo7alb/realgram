from apps.followers.models import Follow
from apps.user.models import Profile, User
from django.contrib.auth.hashers import make_password
from rest_framework import status
from rest_framework.test import APITestCase


class RetrieveFollowTestCase(APITestCase):
	def setUp(self) -> None:
		profile = Profile.objects.create(user=User.objects.create(
			username='doey', 
			email='doey@do.com', 
			first_name='doey', 
			last_name='doey',
			password=make_password('secret')
		))
		follow = Follow.objects.create(
			profile=profile,
			follows=Profile.objects.create(user=User.objects.create(
				username="johndoe",
				first_name="john",
				last_name="johndoe",
				email="johndoe@somemail.com",
				password=make_password('super secret')
			))
		)
		self.url = '/api/follow/{}/'.format(profile.id)
		self.invalid_url = '/api/follow/{}/'.format(profile.id + 120)
		# authenticate user and get authorization toke
		token = self.client.post('/api/profile/authenticate/', {'username': 'doey','password': 'secret'}).json()['token']
		# set up header
		self.header = {'HTTP_AUTHORIZATION': 'Token {}'.format(token)}
		self.validation_profile_id = profile.id

	def tearDown(self) -> None:
		''' flush database once all tests are done '''
		Follow.objects.all().delete()
		Profile.objects.all().delete()
		User.objects.all().delete()

	def test_retrive_follow_list_success(self) -> None:
		''' test if retrieve list returns a status code of 200 '''
		response = self.client.get(self.url, {}, **self.header)
		self.assertEqual(response.status_code, status.HTTP_200_OK)
	
	def test_retrive_follow_list_data(self) -> None:
		''' test if retrieve list returns the correct data '''
		response = self.client.get(self.url, {}, **self.header).json()[0]

		self.assertEqual(response['profile']['id'], self.validation_profile_id)
		
	def test_retrive_follow_invalid_profile(self) -> None:
		''' test if retrieve list returns a status code of 404 for an invalid profile '''
		response = self.client.get(self.invalid_url, {}, **self.header)
		self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

	def test_retrive_follow_unauthorized(self) -> None:
		''' test if retrieve list returns a status code of 401 for an unauthorized profile '''
		response = self.client.get(self.url)
		self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
