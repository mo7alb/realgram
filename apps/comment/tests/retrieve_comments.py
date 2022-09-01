from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from apps.comment.models import Comment
from apps.post.models import Post
from apps.user.models import Profile

class RetrieveCommentsTestCase(APITestCase):
	header = None
	url = ''
	incorrect_url = ''
	post_with_no_comments_url = None

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
		self.client.post('/api/profile/register/', registering_data)
		# authenticate user and get authorization toke
		token = self.client.post('/api/profile/authenticate/', {'username': 'doey','password': 'secret'}).json()['token']
		# set up header
		self.header = {'HTTP_AUTHORIZATION': 'Token {}'.format(token)}

		profile = Profile.objects.get(user=User.objects.get(username='doey', email= 'doey@do.com'))
		post = Post.objects.create(
			profile=profile,
			title="welcome to my website"
		)
		post_with_no_comments = Post.objects.create(
			profile=profile,
			title="welcome to my website"
		)
		Comment.objects.bulk_create([
			Comment(message='Thanks for the welcoming', post=post, profile=profile ),
			Comment(message='anytime',post=post,profile=profile),
			Comment(message='random test',post=post,profile=profile),
		], 3, True)

		self.url = '/api/comments/{}/'.format(post.pk) 
		self.post_with_no_comments_url = '/api/comments/{}/'.format(
			post_with_no_comments.pk
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
