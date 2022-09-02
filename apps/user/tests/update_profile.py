from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase
from apps.user.models import Profile

class ProfileUpdateTestCase(APITestCase):
	url = ''
	header = None
	data = None

	def setUp(self) -> None:
		''' set up common variables for tests to use '''
		register_data = {
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
		
		self.client.post('/api/profile/register/', data=register_data)
		token = self.client.post('/api/profile/authenticate/', data=login_data).json()['token']
		self.header = {'HTTP_AUTHORIZATION': 'Token {}'.format(token)}
		profile = Profile.objects.get(user=User.objects.get(username='cha', email='cha@lie.com'))
		self.url = '/api/profile/{}/'.format(profile.id)

		self.data = {
			'bio': 'super cool guy'
		}

	def tearDown(self) -> None:
		''' clear db once all tests are over '''
		Profile.objects.all().delete()
		User.objects.all().delete()
	
	def test_update_status_code(self) -> None:
		''' test if updating a profile returns a status code of 202 '''
		response = self.client.put(self.url, self.data, **self.header)
		self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
	
	def test_update_invalid_status_code(self) -> None:
		''' test if updating a profile with invalid data returns a status code of 400 '''
		response = self.client.put(self.url, {}, **self.header)
		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
	
	def test_update_unauthorized_status_code(self) -> None:
		''' test if updating a profile while being unauthorized returns a status code of 400 '''
		response = self.client.put(self.url, self.data)
		self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
