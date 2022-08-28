from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from apps.comment.models import Comment
from apps.post.models import Post
from apps.user.models import Profile

class UpdateCommentsTestCase(APITestCase):
	url = ''
	data = None
	incorrect_url = ''
	profile = None 
	post = None 
	comment = None 

	def setUp(self) -> None:
		''' set up variables to be used in tests '''
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
		self.comment = Comment.objects.create(
			message='Thanks for the welcoming',
			post=self.post,
			profile=self.profile
		)
		self.data = { 'message': 'the message has changed'}
		self.url = '/api/comments/{}/'.format(self.comment.pk)
		self.incorrect_url = '/api/comments/{}/'.format(self.comment.pk + 100)

	def tearDown(self) -> None:
		''' clear db once all tests are completed '''
		Comment.objects.all().delete()
		Post.objects.all().delete()
		Profile.objects.all().delete()
		User.objects.all().delete()

	def test_updating_comment_success_status_code(self):
		''' 
		test if updating a comment with correct data returns a status code of 202 
		'''
		response = self.client.put(self.url, self.data)
	
		self.assertEquals(response.status_code, status.HTTP_202_ACCEPTED)
	
	def test_updating_comment_fail_status_code(self):
		''' 
		test if updating a comment that does not exists returns a status code of 404 
		'''
		response = self.client.put(self.incorrect_url, self.data)
	
		self.assertEquals(response.status_code, status.HTTP_404_NOT_FOUND)

	def test_updating_comment_post_fails(self):
		''' test if updating a comment post fails with a status code of 400 '''
		response = self.client.put(self.url, dict(self.data, **{ 'post': 10 }))
		self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)

	def test_updating_comment_profile_fails(self):
		''' test if updating a comment profile fails with a status code of 400 '''
		response = self.client.put(self.url, dict(self.data, **{ 'profile': 10 }))
		self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)

	def test_updating_comment_message_fails(self):
		''' 
		test if updating a comment message to an empty string fails with a status 
		code of 400 
		'''
		response = self.client.put(self.url, {'message': ''})
		self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)

	def test_updating_comment_without_message_fails(self):
		''' 
		test if updating a comment message to an empty string fails with a status 
		code of 400 
		'''
		response = self.client.put(self.url, {})
		self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)

