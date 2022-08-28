from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status

from apps.user.models import User, Profile
from apps.post.models import Post
from apps.comment.models import Comment, LikeComment

class RetrieveCommentLikesTestCase(APITestCase):
	url = ''
	incorrect_url = ''
	profile = None
	comment = None
	comment_without_likes = None
	like = None
	
	def setUp(self) -> None:
		self.profile = Profile.objects.create(
			bio='cool guy',
			user=User.objects.create(
				username='doey',
				email='doey@somedomain.com',
				first_name='doey',
				last_name='johnson'
			)
		)
		
		self.comment = Comment.objects.create(
			profile=self.profile, 
			post=Post.objects.create(profile=self.profile, title='Some post'), 
			message='Some message'
		)
		self.comment_without_likes = Comment.objects.create(
			profile=self.profile, 
			post=Post.objects.create(profile=self.profile, title='Some post'), 
			message='Some other message'
		)
		
		self.like = LikeComment.objects.create(
			comment=self.comment,
			profile=self.profile
		)

		self.url = '/api/like-comment/{}/'.format(self.comment.pk)
		self.incorrect_url = '/api/like-comment/{}/'.format(self.comment.pk + 100)

	def tearDown(self) -> None:
		LikeComment.objects.all().delete()
		Comment .objects.all().delete()
		Post.objects.all().delete()
		Profile.objects.all().delete()
		User .objects.all().delete()

	def test_retrieve_likes_success_status_code(self):
		response = self.client.get(self.url)
		self.assertEqual(response.status_code, status.HTTP_200_OK)
	
	def test_retrieve_likes_success_data(self):
		response = self.client.get(self.url)
		self.assertEqual(response.json(), [{ 'id': self.like.pk }])

	def test_retrieve_likes_fails_status_code(self):
		response = self.client.get(self.incorrect_url)
		self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)