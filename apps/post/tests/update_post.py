from apps.post.models import Post
from apps.user.models import Profile
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase

class PostUpdateTestCase(APITestCase):
	header = None
	url = ''
	data = None
	data_with_profile = None

	def setUp(self) -> None:
		''' set up variables for tests to use them '''
		registering_data = {
			'username': 'doey', 
			'email': 'doey@do.com', 
			'first_name': 'doey', 
			'last_name': 'doey',
			'password': 'secret'
		}
		# register user
		self.client.post('/api/profile/register/', registering_data)
		# authenticate user and get authorization toke
		token = self.client.post('/api/profile/authenticate/', {'username': 'doey','password': 'secret'}).json()['token']
		# set up header
		self.header = {'HTTP_AUTHORIZATION': 'Token {}'.format(token)}

		profile = Profile.objects.get(user=User.objects.get(username='doey', email='doey@do.com'))
		second_profile = Profile.objects.create(
			bio="super cool guy", user=User.objects.create(
				username="johndoe2",
				first_name="john",
				last_name="doe",
				email="johndoe2@somemail.com",
			)
		)
		post = Post.objects.create(profile=profile,title="welcome to my website")

		self.url = '/api/posts/{}/'.format(post.pk)
		self.incorrect_url = '/api/posts/{}/'.format(post.pk + 100)

		self.data = {
			'body': 'Would like to take a moment and thank you'
		}
		self.data_with_profile = {
			'body': 'Would like to take a moment and thank you',
			'profile': second_profile
		}

	def tearDown(self) -> None:
		''' clean the db once the tests are over'''
		Post.objects.all().delete()
		Profile.objects.all().delete()
		User.objects.all().delete()

	def test_update_returns_correct_status(self) -> None:
		''' test if update returns status code 202 on successfull update  '''
		response = self.client.put(self.url, self.data, **self.header)
		self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)

	def test_update_unauthorized_fails(self) -> None:
		''' test if update returns status code 401 when accessed by unauthorized user '''
		response = self.client.put(self.url, self.data)
		self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

	def test_changing_post_profile_fails(self) -> None:
		''' 
		test if trying to update the profile in a post fails with 400 status code 
		'''
		response = self.client.put(self.url, self.data_with_profile, **self.header)

		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
	
	def test_not_passing_anything_fails(self) -> None:
		''' test if an empty dict is passed to as body fails with 400 status code '''
		response = self.client.put(self.url, {}, **self.header)
		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

	def test_incorrect_post_pk_fails(self) -> None:
		''' test if passing an incorrect post pk fails with a 404 error '''
		response = self.client.put(self.incorrect_url, self.data, **self.header)
		self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

