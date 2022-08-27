from apps.post.models import Post, LikePost
from apps.user.models import Profile
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase

class RetrieveLikeTestCase(APITestCase):
	url = ''
	incorrect_url = ''
	first_profile = None
	second_profile = None
	post = None
	Like = None

	def setUp(self) -> None:
		''' set up variables for tests to use them '''
		# first user
		self.first_profile = Profile.objects.create(
			bio="cool guy", 
			user=User.objects.create(
				username="johndoe",
				first_name="john",
				last_name="johndoe",
				email="johndoe@somemail.com"
			)
		)
		
		# second user

		self.second_profile = Profile.objects.create(
			bio="cool guy", 
			user=User.objects.create(
				username="johndoe2",
				first_name="john",
				last_name="johndoe",
				email="johndoe2@somemail.com"
			)
		)
		
		# post
		self.post = Post.objects.create(profile=self.first_profile, title="welcome to my website")
		
		# first like
		self.first_like = LikePost.objects.create(profile=self.first_profile, post=self.post)
		# second like
		self.second_like = LikePost.objects.create(profile=self.second_profile, post=self.post)
		
		# url to retrieve likes
		self.url = '/api/like-post/{}/'.format(self.post.pk)
		# incorrect url to retrieve likes from 
		self.incorrect_url = '/api/like-post/{}/'.format(self.post.pk + 10)
		
	def tearDown(self) -> None:
		''' clean the db once the tests are over'''
		LikePost.objects.all().delete()
		Post.objects.all().delete()
		Profile.objects.all().delete()
		User.objects.all().delete()

	def test_like_retrieve_sucess_code(self):
		''' test if retrieve route returns a status code of 200 '''
		response = self.client.get(self.url)
		self.assertEqual(response.status_code, status.HTTP_200_OK)

	def test_like_retrieve_sucess_data(self):
		''' test if retrieve route returns a status code of 200 '''
		response = self.client.get(self.url).json()
		self.assertEqual(response, [{ 'id': self.first_like.pk }, { 'id': self.second_like.pk },])

	def test_like_retrieve_incorrect_post(self):
		''' test if retrieve route returns a status code of 404 on incorrect post pk passed '''
		response = self.client.get(self.incorrect_url)
		self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
