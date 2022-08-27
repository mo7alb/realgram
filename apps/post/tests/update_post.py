from apps.post.models import Post
from apps.user.models import Profile
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase

class PostUpdateTestCase(APITestCase):
	url = ''
	user = None
	second_user = None
	profile = None
	second_profile = None
	post = None
	data = None
	data_with_profile = None

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
		self.second_user = User.objects.create(
				username="johndoe2",
				first_name="john",
				last_name="doe",
				email="johndoe2@somemail.com",
			)
		self.second_profile = Profile.objects.create(
			bio="super cool guy", 
			user=self.second_user
		)
		self.post = Post.objects.create(
			profile=self.profile,
			title="welcome to my website"
		)
		self.url = '/api/posts/{}/'.format(self.post.pk)
		self.incorrect_url = '/api/posts/{}/'.format(self.post.pk + 100)
		self.data = {
			'body': 'Would like to take a moment and thank you'
		}
		self.data_with_profile = {
			'body': 'Would like to take a moment and thank you',
			'profile': self.second_profile
		}

	def tearDown(self) -> None:
		''' clean the db once the tests are over'''
		Post.objects.all().delete()
		Profile.objects.all().delete()
		User.objects.all().delete()

	def test_update_returns_correct_status(self) -> None:
		''' test if update returns correct status code '''
		response = self.client.put(self.url, self.data)
		self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)

	def test_update_returns_correct_data(self) -> None:
		''' test if updated post has correct data '''
		response = self.client.put(self.url, self.data)
		post = self.client.get(self.url).json()

		self.assertEqual(post['body'], self.data['body'])

	def test_changing_post_profile_fails(self) -> None:
		''' 
		test if trying to update the profile in a post fails with 400 status code 
		'''
		response = self.client.put(self.url, self.data_with_profile)
		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
	
	def test_not_passing_anything_fails(self) -> None:
		''' test if an empty dict is passed to as body fails with 400 status code '''
		response = self.client.put(self.url, {})
		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

	def test_incorrect_post_pk_fails(self) -> None:
		''' test if passing an incorrect post pk fails with a 404 error '''
		response = self.client.put(self.incorrect_url, self.data)
		self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

