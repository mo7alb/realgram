from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from apps.message.models import Room
from apps.user.models import Profile

class NewRoomTestCase(APITestCase):
	header = None
	url = ''
	data = None

	def setUp(self) -> None:
		''' set up variables to be used in tests '''
		# registering data
		registering_data = {
			'username': 'doey', 
			'email': 'doey@do.com', 
			'first_name': 'doey', 
			'last_name': 'doey',
			'password': 'secret'
		}
		# register user
		self.client.post('/api/profile/register/', registering_data)
		self.client.post('/api/profile/register/', {**registering_data, 'username': 'doey1', 'email': 'doey1@do.com'})
		# authenticate user and get authorization toke
		token = self.client.post('/api/profile/authenticate/', {'username': 'doey','password': 'secret'}).json()['token']
		# set up header
		self.header = {'HTTP_AUTHORIZATION': 'Token {}'.format(token)}
		
		profile = Profile.objects.get(user=User.objects.get(username='doey1'))
		self.data = {
			'profile': profile.id
		}
		
		self.url = '/api/message/room/'

	def tearDown(self) -> None:
		Room.objects.all().delete()
		Profile.objects.all().delete()
		User.objects.all().delete()

	def test_new_room_status_code(self) -> None:
		''' test if creating new room returns a status code of 201 '''
		response = self.client.post(self.url, self.data, **self.header)
		self.assertEqual(response.status_code, status.HTTP_201_CREATED)

	def test_new_room_unauthorized_status_code(self) -> None:
		''' test if unauthorized user tries creating a new room returns a status code of 401 '''
		response = self.client.post(self.url, self.data)
		self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

	def test_new_room_enmpty_data_status_code(self) -> None:
		''' test if creating new room with no data returns a status code of 400 '''
		response = self.client.post(self.url, {}, **self.header)
		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

	def test_new_room_invalid_data_status_code(self) -> None:
		''' test if creating new room with invalid profile id returns a status code of 404 '''
		response = self.client.post(self.url, { 'profile': 200 }, **self.header)
		self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

	def test_new_room_twice_status_code(self) -> None:
		''' test if creating new room twice returns a status code of 400 '''
		response = self.client.post(self.url, self.data, **self.header)
		second_response = self.client.post(self.url, self.data, **self.header)
		self.assertEqual(second_response.status_code, status.HTTP_400_BAD_REQUEST)
	