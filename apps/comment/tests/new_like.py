from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status

from apps.user.models import User, Profile
from apps.post.models import Post
from apps.comment.models import Comment, LikeComment

class NewCommentLikeTestCase(APITestCase):
	header = None
	url = ''
	data = None

	def setUp(self) -> None:
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

		profile = Profile.objects.get(pk=profile_id)

		post = Post.objects.create(profile=profile, title='Some post')
		comment = Comment.objects.create(post=post, profile=profile, message='Some message')

		self.data = {'comment':comment.pk, 'profile':profile.id}
		self.url = '/api/like-comment/'

	def tearDown(self) -> None:
		LikeComment.objects.all().delete()
		Comment .objects.all().delete()
		Post.objects.all().delete()
		Profile.objects.all().delete()
		User .objects.all().delete()

	def test_create_new_like_status_code(self):
		''' test if creating a like with correct data returns a status code of 201 '''
		res = self.client.post(self.url, self.data, **self.header)
		self.assertEqual(res.status_code, status.HTTP_201_CREATED)
	
	def test_create_new_like_multiple_times(self):
		''' test if creating a like multiple times returns a status code of 400 '''
		res = self.client.post(self.url, self.data, **self.header)
		res_second = self.client.post(self.url, self.data, **self.header)
		self.assertEqual(res_second.status_code, status.HTTP_400_BAD_REQUEST)
	
	def test_create_new_like_without_comment(self):
		''' test if creating a like without a comment returns a status code of 400 '''
		res = self.client.post(self.url, {'profile': self.data['profile']}, **self.header)
		self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
	
	def test_create_new_like_without_profile(self):
		''' test if creating a like without a profile returns a status code of 400 '''
		res = self.client.post(self.url, {'comment': self.data['comment']}, **self.header)
		self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)