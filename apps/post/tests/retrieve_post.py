from apps.post.models import Post
from apps.user.models import Profile
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase

class PostRetrievalTestCase(APITestCase):
	url = ''
	incorrect_url = ''
	user = None
	profile = None
	post = None

	def setUp(self) -> None:
		''' set up variables for tests to use them '''
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
		''' clean the db once the tests are over'''
		Post.objects.all().delete()
		Profile.objects.all().delete()
		User.objects.all().delete()

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
