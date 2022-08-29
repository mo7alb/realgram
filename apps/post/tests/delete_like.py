from apps.post.models import Post, LikePost
from apps.user.models import Profile
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase

class DeleteLikeTestCase(APITestCase):
	header = None
	url = ''
	incorrect_url = ''
	
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

		# first user
		profile = Profile.objects.get(pk=profile_id)
		
		# post
		post = Post.objects.create(profile=profile, title="welcome to my website")
		
		# first like
		like = LikePost.objects.create(profile=profile, post=post)

		# url to delete like
		self.url = '/api/like-post/{}/'.format(like.pk)
		# set up incorrect url
		self.incorrect_url = '/api/like-post/{}/'.format(like.pk + 10)

	def tearDown(self) -> None:
		''' clean the db once the tests are over'''
		LikePost.objects.all().delete()
		Post.objects.all().delete()
		Profile.objects.all().delete()
		User.objects.all().delete()

	
	def test_delete_like_sucess_code(self):
		''' test if delete route returns a status code of 200 '''
		response = self.client.delete(self.url, {}, **self.header)

		self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)

	def test_delete_like_incorrect_like(self):
		''' test if delete route returns a status code of 404 on incorrect post pk passed '''
		response = self.client.delete(self.incorrect_url, {}, **self.header)
		self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)