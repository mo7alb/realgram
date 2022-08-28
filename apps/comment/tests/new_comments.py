from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from apps.comment.models import Comment
from apps.post.models import Post
from apps.user.models import Profile

class NewCommentsTestCase(APITestCase):
	header = None
	profile_id = None
	url = ''
	data = None
	profile = None
	post = None

	def setUp(self) -> None:
		''' set up variables to be used in tests '''
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


		self.url = '/api/comments/' 
		self.profile = Profile.objects.create(
			bio="cool guy", 
			user=User.objects.create(
				username="johndoe",
				first_name="john",
				last_name="johndoe",
				email="johndoe@somemail.com",
			)
		)
		self.post = Post.objects.create(
			profile=self.profile,
			title="welcome to my website"
		)
		self.data = {
			'message': 'Thank you',
			'post': self.post.pk,
			'profile': self.profile.id
		}
	
	def tearDown(self) -> None:
		''' clear db once all tests are completed '''
		Comment.objects.all().delete()
		Post.objects.all().delete()
		Profile.objects.all().delete()
		User.objects.all().delete()

	def test_adding_new_comment_return_status_code(self) -> None:
		''' test if creating a new comment returns a status code of 201 '''
		response = self.client.post(self.url, self.data, **self.header)
		self.assertEqual(response.status_code, status.HTTP_201_CREATED)

	def test_adding_new_comment_return_data(self) -> None:
		''' test if creating a new comment returns the correct message '''
		response = self.client.post(self.url, self.data, **self.header)
		data = response.json()
		self.assertEqual(data['message'], self.data['message'])
	
	def test_adding_comment_with_missing_profile(self) -> None:
		''' 
		test if creating a new comment without profile returns a status code of 400 
		'''
		response = self.client.post(
			self.url, 
			{
				'message' : 'this is a good post',
				'post': self.post.pk
			}, 
			**self.header
		)
		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
	
	def test_adding_comment_with_missing_post(self) -> None:
		''' 
		test if creating a new comment without post returns a status code of 400 
		'''
		response = self.client.post(
			self.url, 
			{
				'message' : 'this is a good post',
				'profile': self.profile.id
			}, 
			**self.header
		)
		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

	def test_adding_comment_with_missing_message(self) -> None:
		''' 
		test if creating a new comment without message returns a status code of 400 
		'''
		response = self.client.post(
			self.url, 
			{
				'profile': self.profile.id,
				'post': self.post.pk
			}, 
			**self.header
		)
		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

	def test_adding_comment_with_incorrect_post(self) -> None:
		''' 
		test if creating a new comment with incorrect post returns a status code of 404
		'''
		response = self.client.post(
			self.url, 
			{
				'message' : 'this is a good post',
				'profile': self.profile.id,
				'post': self.post.pk + 10
			}, 
			**self.header
		)
		self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
	
	def test_adding_comment_with_incorrect_profile(self) -> None:
		''' 
		test if creating a new comment with incorrect profile returns a status code of 404
		'''
		response = self.client.post(
			self.url, 
			{
				'message' : 'this is a good post',
				'profile': self.profile.id + 120,
				'post': self.post.pk
			},
			**self.header
		)
		self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
