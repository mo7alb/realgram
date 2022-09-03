from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from apps.message.models import Room
from apps.user.models import Profile

class RetrieveRoomTestCase(APITestCase):
	header = None
	url = ''
	data = None

	def setUp(self) -> None:
		''' set up variables to be used in tests '''
		# registering data
		registering_data = {'username': 'doey', 'email': 'doey@do.com', 'first_name': 'doey', 'last_name': 'doey','password': 'secret'}
		registering_data_2 = {'username': 'doey1', 'email': 'doey1@do.com', 'first_name': 'doey', 'last_name': 'doey','password': 'secret'}
		# register user
		self.client.post('/api/profile/register/', registering_data)
		self.client.post('/api/profile/register/', registering_data_2)
		# authenticate user and get authorization toke
		token = self.client.post('/api/profile/authenticate/', {'username': 'doey','password': 'secret'}).json()['token']
		# set up header
		self.header = {'HTTP_AUTHORIZATION': 'Token {}'.format(token)}
		profile = Profile.objects.get(user=User.objects.get(username='doey1'))

		self.client.post('/api/message/room/', { 'profile': profile.id }, **self.header)
		
		self.url = '/api/message/room/{}/'.format(profile.id)

	def tearDown(self) -> None:
		Room.objects.all().delete()
		Profile.objects.all().delete()
		User.objects.all().delete()

	def test_retrieve_room_status_code(self) -> None:
		''' test if retrieving a room returns a status code of 200 '''
		response = self.client.get(self.url, {}, **self.header)
		self.assertEqual(response.status_code, status.HTTP_200_OK)

	def test_retrieve_room_status_code_invalid_url(self) -> None:
		''' test if retrieving a room with invalid url returns a status code of 404 '''
		response = self.client.get('/api/message/room/10000/', {}, **self.header)
		self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

	def test_retrieve_room_status_code_unauthorized(self) -> None:
		''' test if retrieving a room unauthorized returns a status code of 401 '''
		response = self.client.get(self.url)
		self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)