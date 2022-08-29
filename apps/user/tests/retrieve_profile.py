
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase
from apps.user.models import Profile

class ProfileRetreivalTestCase(APITestCase):
	url = ''
	header = None

	def setUp(self) -> None:
		self.base_url = '/api/profile/'
		self.data = {
			'username': 'cha',
			'email': 'cha@lie.com',
			'first_name': 'charlie',
			'last_name': 'doe',
			'password': 'super secret',
		}
		login_data = {
			'username': 'cha',
			'password': 'super secret',
		}
		
		register_response = self.client.post('/api/profile/register/', data=self.data).json()['profile']
		token = self.client.post('/api/profile/authenticate/', data=login_data).json()['token']
		self.header = {'HTTP_AUTHORIZATION': 'Token {}'.format(token)}
		self.url = '/api/profile/{}/'.format(register_response['id'])

	def tearDown(self) -> None:
		Profile.objects.all().delete()
		User.objects.all().delete()
	
	def test_retrieve_route_correct_status_code(self):
		''' test if retrieving a user returns a success code of 200 '''
		retrieve = self.client.get(self.url, {}, **self.header)

		self.assertEqual(retrieve.status_code, status.HTTP_200_OK)
	
	def test_retrieve_route_correct_data(self):
		''' test if retrieving returns correct username and password'''
		retrieve = self.client.get(self.url,{},**self.header)
		res_data = retrieve.json()
		res_user = {
			'username': res_data['user']['username'],
			'email': res_data['user']['email']
		}
		data = { 'username': 'cha','email': 'cha@lie.com' }

		self.assertEqual(res_user, data)
	
	def test_retrieve_route_incorrect_status_code(self):
		''' test if retrieving invalid user returns a status code of 404 '''
		url = '/api/profile/100/'
		retrieve = self.client.get(url, {}, **self.header)

		self.assertEqual(retrieve.status_code, status.HTTP_404_NOT_FOUND)
	
	def test_unauthorized_profile_retrieval(self):
		''' 
		test if retrieving a profile while being unauthorized returns 
		status code of 401 
		'''
		retrieve = self.client.get(self.url)

		self.assertEqual(retrieve.status_code, status.HTTP_401_UNAUTHORIZED)
