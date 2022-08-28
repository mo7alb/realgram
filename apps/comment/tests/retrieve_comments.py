from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from apps.comment.models import Comment
from apps.post.models import Post
from apps.user.models import Profile

class RetrieveCommentsTestCase(APITestCase):
	header = None
	profile_id = None
	url = ''
	incorrect_url = ''
	profile = None
	post = None
	post_with_no_comments = None
	first_comment = None
	second_comment = None
	third_comment = None

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
		self.post_with_no_comments = Post.objects.create(
			profile=self.profile,
			title="welcome to my website"
		)
		self.first_comment = Comment.objects.create(
			message='Thanks for the welcoming',
			post=self.post,
			profile=self.profile
		)
		self.second_comment = Comment.objects.create(
			message='anytime',
			post=self.post,
			profile=self.profile
		)
		self.third_comment = Comment.objects.create(
			message='testing comment section',
			post=self.post,
			profile=self.profile
		)

		self.url = '/api/comments/{}/'.format(self.post.pk) 
		self.post_with_no_comments_url = '/api/comments/{}/'.format(
			self.post_with_no_comments.pk
		) 
		self.incorrect_post_url = '/api/comments/300/'
	
	def tearDown(self) -> None:
		''' clear db once all tests are completed '''
		Comment.objects.all().delete()
		Post.objects.all().delete()
		Profile.objects.all().delete()
		User.objects.all().delete()

	def test_retrieving_comments_return_status_code(self) -> None:
		''' test if retrieving a list of comment returns a status code of 200 '''
		response = self.client.get(self.url, {}, **self.header)
		self.assertEqual(response.status_code, status.HTTP_200_OK)

	def test_retrieving_comments_return_error_status_code(self) -> None:
		''' test if creating a new comment returns a status code of 404 '''
		response = self.client.get(self.incorrect_post_url, {}, **self.header)
		
		self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

	def test_retrieving_(self) -> None:
		''' test if creating a new comment returns a status code of 404 '''
		response = self.client.get(self.post_with_no_comments_url, {}, **self.header)
		
		self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
