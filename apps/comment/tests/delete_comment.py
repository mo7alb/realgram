from urllib import response
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from apps.comment.models import Comment
from apps.post.models import Post
from apps.user.models import Profile

class DeleteCommentsTestCase(APITestCase):
	url = ''
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
		self.url = '/api/comments/{}/'.format(self.comment.pk)
		self.incorrect_url = '/api/comments/{}/'.format(self.comment.pk + 10)

	def tearDown(self) -> None:
		''' clear db once all tests are completed '''
		Comment.objects.all().delete()
		Post.objects.all().delete()
		Profile.objects.all().delete()
		User.objects.all().delete()

	def test_deleting_comment_success_status_code(self) -> None:
		''' test if deleting a comment returns a status code of 202 '''
		response = self.client.delete(self.url)

		self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)

	def test_deleting_comment_fail_status_code(self) -> None:
		''' 
		test if trying to delete a comment that does not exists a status code of 404 
		'''
		response = self.client.delete(self.incorrect_url)

		self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
