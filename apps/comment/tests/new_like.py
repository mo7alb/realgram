from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status

from apps.user.models import User, Profile
from apps.post.models import Post
from apps.comment.models import Comment, LikeComment

class NewCommentLikeTestCase(APITestCase):
	url = ''
	profile = None
	post = None
	comment = None
	data = None

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

		self.data = {'comment':self.comment.pk, 'profile':self.profile.id}
		self.url = '/api/like-comment/'

	def tearDown(self) -> None:
		LikeComment.objects.all().delete()
		Comment .objects.all().delete()
		Post.objects.all().delete()
		Profile.objects.all().delete()
		User .objects.all().delete()

	def test_create_new_like_status_code(self):
		''' test if creating a like with correct data returns a status code of 201 '''
		res = self.client.post(self.url, self.data)
		self.assertEqual(res.status_code, status.HTTP_201_CREATED)
	
	def test_create_new_like_multiple_times(self):
		''' test if creating a like multiple times returns a status code of 400 '''
		res = self.client.post(self.url, self.data)
		res_second = self.client.post(self.url, self.data)
		self.assertEqual(res_second.status_code, status.HTTP_400_BAD_REQUEST)
	
	def test_create_new_like_without_comment(self):
		''' test if creating a like without a comment returns a status code of 400 '''
		res = self.client.post(self.url, {'profile': self.data['profile']})
		self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
	
	def test_create_new_like_without_profile(self):
		''' test if creating a like without a profile returns a status code of 400 '''
		res = self.client.post(self.url, {'comment': self.data['comment']})
		self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)