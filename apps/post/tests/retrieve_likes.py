from apps.post.models import Post, LikePost
from apps.user.models import Profile
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase

class RetrieveLikeTestCase(APITestCase):
	header = None
	url = ''
	incorrect_url = ''
	first_like = None
	second_like = None

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
		first_profile = Profile.objects.get(pk=profile_id)
		# second profile
		second_profile = Profile.objects.create(
			bio="cool guy", user=User.objects.create(
				username="johndoe2",
				first_name="john",
				last_name="johndoe",
				email="johndoe2@somemail.com"
			)
		)
		
		# post
		post = Post.objects.create(profile=first_profile, title="welcome to my website")
		
		# first like
		self.first_like = LikePost.objects.create(profile=first_profile, post=post)
		# second like
		self.second_like = LikePost.objects.create(profile=second_profile, post=post)
		
		# url to retrieve likes
		self.url = '/api/like-post/{}/'.format(post.pk)
		# incorrect url to retrieve likes from 
		self.incorrect_url = '/api/like-post/{}/'.format(post.pk + 10)
		
	def tearDown(self) -> None:
		''' clean the db once the tests are over'''
		LikePost.objects.all().delete()
		Post.objects.all().delete()
		Profile.objects.all().delete()
		User.objects.all().delete()

	def test_like_retrieve_sucess_code(self):
		''' test if retrieve route returns a status code of 200 '''
		response = self.client.get(self.url, {}, **self.header)
		self.assertEqual(response.status_code, status.HTTP_200_OK)

	def test_like_retrieve_sucess_data(self):
		''' test if retrieve route returns a status code of 200 '''
		response = self.client.get(self.url, {}, **self.header).json()
		self.assertEqual(response, [{ 'id': self.first_like.pk }, { 'id': self.second_like.pk },])

	def test_like_retrieve_incorrect_post(self):
		''' test if retrieve route returns a status code of 404 on incorrect post pk passed '''
		response = self.client.get(self.incorrect_url, {}, **self.header)
		self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
