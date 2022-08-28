from apps.post.models import Post
from apps.user.models import Profile
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase

class DeletePostTestCase(APITestCase):
	header = None
	profile_id = None
	url = ''
	incorrect_url = ''
	user = None
	profile = None
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
		self.profile_id = self.client.post('/api/profile/register/', registering_data).json()['profile']['id']
		# authenticate user and get authorization toke
		token = self.client.post('/api/profile/authenticate/', {'username': 'doey','password': 'secret'}).json()['token']
		# set up header
		self.header = {'HTTP_AUTHORIZATION': 'Token {}'.format(token)}

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
		self.incorrect_url = '/api/posts/100000/'
		
	def tearDown(self) -> None:
		''' clean the db once the tests are over'''
		Post.objects.all().delete()
		Profile.objects.all().delete()
		User.objects.all().delete()

	def test_post_delete_sucess(self) -> None:
		''' test if deleting an exisiting post successfully returns a status of 202 '''
		response = self.client.delete(self.url, {}, **self.header)
		self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

	def test_post_delete_fail(self) -> None:
		''' tests if deleting a post that does not exisits returns a status of 404 '''
		response = self.client.delete(self.incorrect_url, {}, **self.header)
		self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

	def test_access_post_after_deleting_fails(self) -> None:
		''' test if accessing a post after deleting it fails '''
		response = self.client.delete(self.url, {}, **self.header)
		response_retrieving = self.client.get(self.url, {}, **self.header)

		self.assertEqual(response_retrieving.status_code, status.HTTP_404_NOT_FOUND)
