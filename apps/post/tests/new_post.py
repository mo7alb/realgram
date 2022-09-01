from apps.post.models import Post
from apps.user.models import Profile
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase


class NewPostTestCase(APITestCase):
	header = None
	url = ''
	data = None
	data_without_title = None
	data_incorrect_profile_id = None

	def setUp(self) -> None:
		# data for user registration
		registering_data = {
			'username': 'doey', 
			'email': 'doey@do.com', 
			'first_name': 'doey', 
			'last_name': 'doey',
			'password': 'secret'
		}
		# register user
		self.client.post('/api/profile/register/', registering_data)
		# authenticate user and get authorization toke
		token = self.client.post('/api/profile/authenticate/', {'username': 'doey','password': 'secret'}).json()['token']
		# set up header
		self.header = {'HTTP_AUTHORIZATION': 'Token {}'.format(token)}

		self.url = '/api/posts/'		
		self.data = {
			'title': 'this is a post',
			'caption': 'Check this cool post'
		}
		self.data_without_title = { 'caption': 'this is a cool post' }
	
	def tearDown(self) -> None:
		Post.objects.all().delete()
		Profile.objects.all().delete()
		User.objects.all().delete()

	def test_new_post_status_code_correct(self):
		''' test if creating a new post returns a status code of 201 '''
		response = self.client.post(self.url, self.data, **self.header)
		
		self.assertEqual(response.status_code, status.HTTP_201_CREATED)

	def test_new_post_unauthorized_status_code_correct(self):
		''' test if unauthorized user tries creating a new post returns a status code of 401 '''
		response = self.client.post(self.url, self.data)
		
		self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
	
	def test_new_post_status_code_incorrect(self):
		''' test if creating a new post returns a status code of 400 if title is not passed '''
		response = self.client.post(self.url, self.data_without_title, **self.header)
		
		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
