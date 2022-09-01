from apps.post.models import Post, LikePost
from apps.user.models import Profile
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase

class CreateLikeTestCase(APITestCase):
	header = None
	url = ''
	profile = None
	post = None
	data = None
	data_invalid_post = None
	data_invalid_profile = None

	def setUp(self) -> None:
		''' set up variables for tests to use them '''
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

		self.profile = profile = Profile.objects.get(user=User.objects.get(username='doey', email='doey@do.com'))

		self.post = Post.objects.create(
			profile=self.profile,
			title="welcome to my website"
		)
		self.url = '/api/like-post/'
		self.data = { 'post': self.post.pk, 'profile': self.profile.pk }
		self.data_invalid_post = { 'post': self.post.pk + 10 , 'profile': self.profile.pk }
		self.data_invalid_profile = { 'post': self.post.pk , 'profile': self.profile.pk + 10 }
		
	def tearDown(self) -> None:
		''' clean the db once the tests are over'''
		LikePost.objects.all().delete()
		Post.objects.all().delete()
		Profile.objects.all().delete()
		User.objects.all().delete()

	def test_create_like_success_code(self):
		''' test if creating like returns correct status code '''
		response = self.client.post(self.url, self.data, **self.header)
		self.assertEqual(response.status_code, status.HTTP_201_CREATED)
	
	def test_create_like_invalid_post_data(self):
		''' test if sending incorrect post data returns 404 error '''
		response = self.client.post(self.url, self.data_invalid_post, **self.header)
		self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
	
	def test_create_like_invalid_profle_data(self):
		''' test if sending incorrect profile data returns 404 error '''
		response = self.client.post(self.url, self.data_invalid_profile, **self.header)
		self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

	def test_create_like_unauthorized_fails(self):
		''' test if creating a like fails with an status code of 401 for an unauthorized request '''
		response = self.client.post(self.url, self.data)
		self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
