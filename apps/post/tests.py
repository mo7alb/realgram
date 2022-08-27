from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APITestCase

from apps.post.model_factories import PostFactory, ProfileFactory, UserFactory
from apps.post.models import Post
from apps.user.models import Profile

class NewPostTestCase(APITestCase):
	url = ''
	data = None
	user = None
	profile = None
	data_without_title = None
	data_incorrect_profile_id = None

	def setUp(self) -> None:
		self.url = '/api/posts/'
		self.user = User.objects.create(
			username='doey', 
			email='doey@do.com', 
			first_name='doey', 
			last_name='doey'
		)
		self.profile = Profile.objects.create(user=self.user, bio="A guy with lots of potential")
		self.data = {
			'profile': self.profile.id,
			'title': 'this is a post',
			'caption': 'Check this cool post'
		}
		self.data_without_title = { 'profile': self.profile.id, 'caption': 'this is a cool post' }
		self.data_incorrect_profile_id = {
			'title': 'Check out this lemur', 
			'caption': 'this is a cool post',
			'profile': 1000
		}
	
	def tearDown(self) -> None:
		Post.objects.all().delete()
		Profile.objects.all().delete()
		User.objects.all().delete()

	def test_new_post_status_code_correct_data(self):
		''' test if creating a new post returns a status code of 201 '''
		response = self.client.post(self.url, self.data)
		
		self.assertEqual(response.status_code, status.HTTP_201_CREATED)
	
	def test_new_post_status_code_incorrect_data(self):
		''' test if creating a new post returns a status code of 201 '''
		response = self.client.post(self.url, self.data_without_title)
		
		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
	
	def test_new_post_status_code_incorrect_profile(self):
		''' test if creating a new post returns a status code of 201 '''
		response = self.client.post(self.url, self.data_incorrect_profile_id)
		
		self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

	def test_new_post_data_returned_correct_data(self):
		''' test if creating a new post returns a status code of 201 '''
		response = self.client.post(self.url, self.data)
		data = response.json()
		self.assertEqual(data['title'], self.data['title'])

class PostListTestCase(APITestCase):
	url = ''
	user = None
	profile = None
	post = None

	def setUp(self) -> None:
		self.url = '/api/posts/'
		self.user = User.objects.create(
				username="johndoe",
				first_name="john",
				last_name="johndoe",
				email="johndoe@somemail.com",
			)
		self.profile = Profile.objects.create(
			bio="cool guy", 
			user=self.user
		)
		self.post = Post.objects.create(
			profile=self.profile,
			title="welcome to my website"
		)

	def tearDown(self) -> None:
		Post.objects.all().delete()
		Profile.objects.all().delete()
		User.objects.all().delete()

		PostFactory.reset_sequence(0)
		ProfileFactory.reset_sequence(0)
		UserFactory.reset_sequence(0)

	def test_list_route_returns_success_code(self):
		''' check if the posts list route returns a status code of 200 '''
		response = self.client.get(self.url)

		self.assertEqual(response.status_code, status.HTTP_200_OK)

	def test_list_route_returns_correct_title(self):
		''' check if the posts list route returns correct data by checking the returned title '''
		response = self.client.get(self.url)
		data = response.json()

		self.assertEqual(data[0]['title'], self.post.title)
	
	def test_list_route_returns_correct_profile(self):
		''' check if the posts list route returns correct data by checking the returned title '''
		response = self.client.get(self.url)
		data = response.json()[0]['profile']

		self.assertEqual(data, { 'id': self.profile.id, 'user': { 'username': self.user.username}})

class PostRetrievalTestCase(APITestCase):
	url = ''
	incorrect_url = ''
	user = None
	profile = None
	post = None

	def setUp(self) -> None:
		self.user = User.objects.create(
				username="johndoe",
				first_name="john",
				last_name="johndoe",
				email="johndoe@somemail.com",
			)
		self.profile = Profile.objects.create(
			bio="cool guy", 
			user=self.user
		)
		self.post = Post.objects.create(
			profile=self.profile,
			title="welcome to my website"
		)
		self.url = '/api/posts/{}/'.format(self.post.pk)
		self.incorrect_url = '/api/posts/140/'

	def tearDown(self) -> None:
		Post.objects.all().delete()
		Profile.objects.all().delete()
		User.objects.all().delete()

		PostFactory.reset_sequence(0)
		ProfileFactory.reset_sequence(0)
		UserFactory.reset_sequence(0)

	def test_retrieval_route_status_code_correct_url(self):
		''' check if route returns 200 status code on correct url '''
		response = self.client.get(self.url)

		self.assertEqual(response.status_code, status.HTTP_200_OK)
	
	def test_retrieval_route_status_code_incorrect_url(self):
		''' check if retrieve route returns 404 status code on incorrect url '''
		response = self.client.get(self.incorrect_url)

		self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

	def test_retrieval_route_data(self):
		''' check if route returns 200 status code on correct url '''
		response = self.client.get(self.url)
		data = response.json()

		self.assertEqual(data['title'], self.post.title)
