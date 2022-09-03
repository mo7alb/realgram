
from apps.message.models import Message
from apps.user.models import Profile
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase

class RetrieveMessageTestCase(APITestCase):
	header = None
	url = ''

	def setUp(self) -> None:
		''' set up variables for tests to use them '''
		registering_data = {
			'username': 'doey', 
			'email': 'doey@do.com', 
			'first_name': 'doey', 
			'last_name': 'doey',
			'password': 'secret'
		}
		registering_data_2 = {
			'username': 'doey1', 
			'email': 'doey1@do.com', 
			'first_name': 'doey', 
			'last_name': 'doey',
			'password': 'secret'
		}
		# register first user
		self.client.post('/api/profile/register/', registering_data)
		# register second user
		self.client.post('/api/profile/register/', registering_data_2)
		# authenticate user and get authorization toke
		token = self.client.post('/api/profile/authenticate/', {'username': 'doey','password': 'secret'}).json()['token']
		# set up header
		self.header = {'HTTP_AUTHORIZATION': 'Token {}'.format(token)}

		reciever = Profile.objects.get(user=User.objects.get(username='doey1', email='doey1@do.com'))

		self.url = '/api/messages/{}/'.format(reciever.id)

		self.client.post('/api/messages/', { 'reciever': reciever.id, 'message': 'hey'}, **self.header)

	def tearDown(self) -> None:
		''' clean the db once the tests are over'''
		Message.objects.all().delete()
		Profile.objects.all().delete()
		User.objects.all().delete()

	def test_retrieve_message_status_code(self) -> None:
		''' test if retrieving a messages list returns a status code of 200 '''
		response = self.client.get(self.url, {}, **self.header)
		self.assertEqual(response.status_code, status.HTTP_200_OK)

	def test_retrieve_message_invalid_url(self) -> None:
		''' 
		test if retrieving a messages list with an invalid url returns 
		a status code of 200
		'''
		response = self.client.get('/api/messages/1200/', {}, **self.header)
		self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

	def test_retrieve_message_unauthorized(self) -> None:
		''' 
		test if retrieving a messages list with an invalid url returns 
		a status code of 200
		'''
		response = self.client.get(self.url)
		self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)