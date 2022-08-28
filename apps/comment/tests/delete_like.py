from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status

from apps.user.models import User, Profile
from apps.post.models import Post
from apps.comment.models import Comment, LikeComment

class deleteCommentLikeTestCase(APITestCase):
	url = ''
	incorrect_url = ''
	profile = None
	post = None
	comment = None
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

		self.post = Post.objects.create(profile=self.profile, title='Some post')
		self.comment = Comment.objects.create(post=self.post, profile=self.profile, message='Some message')
		self.like = LikeComment.objects.create(comment=self.comment, profile=self.profile)

		self.url = '/api/like-comment/{}/'.format(self.like.pk)
		self.incorrect_url = '/api/like-comment/{}/'.format(self.like.pk + 100)

	def tearDown(self) -> None:
		LikeComment.objects.all().delete()
		Comment .objects.all().delete()
		Post.objects.all().delete()
		Profile.objects.all().delete()
		User .objects.all().delete()

	def test_delete_like_success(self):
		''' test if successfully deleting a like returns a status code of 204 '''
		response = self.client.delete(self.url)
		self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

	def test_delete_like_fail(self):
		''' test if deleting a like that does not exists returns a status code of 404 '''
		response = self.client.delete('/api/like-comment/12000/')
		self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)