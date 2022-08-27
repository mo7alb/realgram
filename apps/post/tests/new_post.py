from apps.post.models import Post
from apps.user.models import Profile
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase


class NewPostTestCase(APITestCase):
	url = ''
	data = None
	user = None
	profile = None
	data_without_title = None
	data_incorrect_profile_id = None

	def setUp(self) -> None:
		self.url = '/api/posts/'
		self.user = User.objects.create(
			username='doey', 
			email='doey@do.com', 
			first_name='doey', 
			last_name='doey'
		)
		self.profile = Profile.objects.create(user=self.user, bio="A guy with lots of potential")
		self.data = {
			'profile': self.profile.id,
			'title': 'this is a post',
			'caption': 'Check this cool post'
		}
		self.data_without_title = { 'profile': self.profile.id, 'caption': 'this is a cool post' }
		self.data_incorrect_profile_id = {
			'title': 'Check out this lemur', 
			'caption': 'this is a cool post',
			'profile': 1000
		}
	
	def tearDown(self) -> None:
		Post.objects.all().delete()
		Profile.objects.all().delete()
		User.objects.all().delete()

	def test_new_post_status_code_correct_data(self):
		''' test if creating a new post returns a status code of 201 '''
		response = self.client.post(self.url, self.data)
		
		self.assertEqual(response.status_code, status.HTTP_201_CREATED)
	
	def test_new_post_status_code_incorrect_data(self):
		''' test if creating a new post returns a status code of 201 '''
		response = self.client.post(self.url, self.data_without_title)
		
		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
	
	def test_new_post_status_code_incorrect_profile(self):
		''' test if creating a new post returns a status code of 201 '''
		response = self.client.post(self.url, self.data_incorrect_profile_id)
		
		self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

	def test_new_post_data_returned_correct_data(self):
		''' test if creating a new post returns a status code of 201 '''
		response = self.client.post(self.url, self.data)
		data = response.json()
		self.assertEqual(data['title'], self.data['title'])
