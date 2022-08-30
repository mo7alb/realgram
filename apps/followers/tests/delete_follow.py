from django.contrib.auth.hashers import make_password
from apps.user.models import Profile, User
from apps.followers.models import Follow
from rest_framework import status
from rest_framework.test import APITestCase

class DeleteFollowTestCase(APITestCase):
	def setUp(self) -> None:
		''' set up variables to be used in tests '''
		follow = Follow.objects.create(
				profile=Profile.objects.create(user=User.objects.create(
				username='doey', 
				email='doey@do.com', 
				first_name='doey', 
				last_name='doey',
				password=make_password('secret')
			)),
			follows=Profile.objects.create(user=User.objects.create(
				username="johndoe",
				first_name="john",
				last_name="johndoe",
				email="johndoe@somemail.com",
				password=make_password('super secret')
			))
		)
		self.url = '/api/follow/{}/'.format(follow.pk)
		self.invalid_url = '/api/follow/{}/'.format(follow.pk + 120)
		# authenticate user and get authorization toke
		token = self.client.post('/api/profile/authenticate/', {'username': 'doey','password': 'secret'}).json()['token']
		# set up header
		self.header = {'HTTP_AUTHORIZATION': 'Token {}'.format(token)}

	def tearDown(self) -> None:
		''' flush database once all tests are done '''
		Follow.objects.all().delete()
		Profile.objects.all().delete()
		User.objects.all().delete()

	def test_unauthorized_follow_delete(self) -> None:
		''' test if deleting a follow while being unauthorized returns a 401 error '''
		response = self.client.delete(self.url)
		self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

	def test_follow_delete_valid_url(self) -> None:
		''' test if deleting a follow returns a status code of 204 '''
		response = self.client.delete(self.url, {}, **self.header)
		self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

	def test_follow_delete_invalid_url(self) -> None:
		''' test if deleting a follow returns a status code of 404 if the follow does not exists '''
		response = self.client.delete(self.invalid_url, {}, **self.header)
		self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
