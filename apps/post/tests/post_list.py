from apps.post.models import Post
from apps.user.models import Profile
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase

class PostListTestCase(APITestCase):
	header = None
	profile = None
	url = ''
	
	def setUp(self) -> None:
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
		self.profile = Profile.objects.get(user=User.objects.get(username='doey', email='doey@do.com'))
		self.post = Post.objects.create(profile=self.profile,title="welcome to my website")

	def tearDown(self) -> None:
		Post.objects.all().delete()
		Profile.objects.all().delete()
		User.objects.all().delete()

	def test_list_route_returns_success_code(self):
		''' check if the posts list route returns a status code of 200 '''
		response = self.client.get(self.url, {}, **self.header)

		self.assertEqual(response.status_code, status.HTTP_200_OK)

	def test_list_route_unauthorized_fails(self):
		''' check if the posts list route returns a status code of 401 for unauthorized users '''
		response = self.client.get(self.url)

		self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

	def test_list_route_returns_correct_title(self):
		''' check if the posts list route returns correct data by checking the returned title '''
		response = self.client.get(self.url, {}, **self.header)
		data = response.json()

		self.assertEqual(data[0]['title'], self.post.title)
	
	def test_list_route_returns_correct_profile(self):
		''' check if the posts list route returns correct data by checking the returned title '''
		response = self.client.get(self.url, {}, **self.header)
		data = response.json()[0]['profile']
		
		self.assertEqual(data['id'], self.profile.id)
