from apps.post.models import Post, LikePost
from apps.user.models import Profile
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase

class CreateLikeTestCase(APITestCase):
	url = ''
	user = None
	profile = None
	post = None
	Like = None

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
		self.url = '/api/like-post/'
		
	def tearDown(self) -> None:
		''' clean the db once the tests are over'''
		LikePost.objects.all().delete()
		Post.objects.all().delete()
		Profile.objects.all().delete()
		User.objects.all().delete()

	def test_create_like_success_code(self):
		''' test if creating like returns correct status code '''
		response = self.client.post(self.url, { 'post': self.post.pk, 'profile': self.profile.pk })
		self.assertEqual(response.status_code, status.HTTP_201_CREATED)
	
	def test_create_like_invalid_post_data(self):
		''' test if sending incorrect post data returns 404 error '''
		response = self.client.post(self.url, { 'post': self.post.pk + 10 , 'profile': self.profile.pk })
		self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
	
	def test_create_like_invalid_profle_data(self):
		''' test if sending incorrect profile data returns 404 error '''
		response = self.client.post(self.url, { 'post': self.post.pk , 'profile': self.profile.pk + 10 })
		self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)