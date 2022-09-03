from urllib import response
from apps.message.models import Message
from apps.user.models import Profile
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase

class NewMessageTestCase(APITestCase):
	header = None
	url = ''
	data = None
	profile_id = None

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

		self.profile_id = Profile.objects.get(user=User.objects.get(username='doey', email='doey@do.com')).id
		self.url = '/api/messages/'

		self.data = {
			'message': 'hey', 'reciever': self.profile_id
		}
		
	def tearDown(self) -> None:
		''' clean the db once the tests are over'''
		Message.objects.all().delete()
		Profile.objects.all().delete()
		User.objects.all().delete()

	def test_new_message_status_code(self) -> None:
		''' test if creating a new message returns a status code of 201 '''
		response = self.client.post(self.url, self.data, **self.header)
		self.assertEqual(response.status_code, status.HTTP_201_CREATED)

	def test_new_message_unauthorized_status_code(self) -> None:
		''' test if creating a new message unauthorized returns a status code of 401 '''
		response = self.client.post(self.url, self.data)
		self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

	def test_new_message_incorrect_data_status_code(self) -> None:
		''' 
		test if creating a new message or reciever without message returns a status code of 400
		'''
		response = self.client.post(self.url, {}, **self.header)
		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
	
	def test_new_message_without_message_status_code(self) -> None:
		''' 
		test if creating a new message without message returns a status code of 400
		'''
		response = self.client.post(self.url, {'reciever': self.profile_id}, **self.header)
		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

	def test_new_message_without_reciever_status_code(self) -> None:
		''' 
		test if creating a new message without reciever returns a status code of 400
		'''
		response = self.client.post(self.url, {'message': 'hey'}, **self.header)
		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)