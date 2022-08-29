from apps.post.models import Post
from apps.user.models import Profile
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase

class PostRetrievalTestCase(APITestCase):
	header = None
	url = ''
	incorrect_url = ''
	post = None

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
		profile_id = self.client.post('/api/profile/register/', registering_data).json()['profile']['id']
		# authenticate user and get authorization toke
		token = self.client.post('/api/profile/authenticate/', {'username': 'doey','password': 'secret'}).json()['token']
		# set up header
		self.header = {'HTTP_AUTHORIZATION': 'Token {}'.format(token)}

		profile = Profile.objects.get(pk=profile_id)

		self.post = Post.objects.create(
			profile=profile,
			title="welcome to my website"
		)
		self.url = '/api/posts/{}/'.format(self.post.pk)
		self.incorrect_url = '/api/posts/140/'

	def tearDown(self) -> None:
		''' clean the db once the tests are over'''
		Post.objects.all().delete()
		Profile.objects.all().delete()
		User.objects.all().delete()

	def test_retrieval_route_status_code_correct_url(self):
		''' check if route returns 200 status code on correct url '''
		response = self.client.get(self.url, {}, **self.header)

		self.assertEqual(response.status_code, status.HTTP_200_OK)

	def test_retrieval_route_status_code_unauthorized(self):
		''' check if route returns 401 status code when accessed by unauthorized user '''
		response = self.client.get(self.url)

		self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
	
	def test_retrieval_route_status_code_incorrect_url(self):
		''' check if retrieve route returns 404 status code on incorrect url '''
		response = self.client.get(self.incorrect_url, {}, **self.header)

		self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

	def test_retrieval_route_data(self):
		''' check if route returns 200 status code on correct url '''
		response = self.client.get(self.url, {}, **self.header)
		data = response.json()

		self.assertEqual(data['title'], self.post.title)

