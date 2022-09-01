from apps.user.models import Profile, User
from rest_framework import status
from rest_framework.test import APITestCase

class RegistrationTestCase(APITestCase):
	''' test if a new user can register '''
	url = ''
	data = None
	incorrect_data = None
	
	def setUp(self) -> None:
		''' set up variables to be used in the tests '''
		# url to register user
		self.url = '/api/profile/register/'
		# incorrect registration data
		self.incorrect_data = {
			'username': 'johndoe',
			'first_name': 'john'
		}
		# registration data
		self.data = {
			'username': 'cha',
			'email': 'cha@lie.com',
			'first_name': 'charlie',
			'last_name': 'doe',
			'password': 'super secret',
		}

	def tearDown(self) -> None:
		''' clear all tables once all tests are over '''
		Profile.objects.all().delete()
		User.objects.all().delete()

	def test_registration(self) -> None:
		''' test to check if correct status code is returned on sending correct data to API '''
		# register with correct data
		response = self.client.post(self.url, data=self.data)
		# assert if response status code is 201
		self.assertEqual(response.status_code, status.HTTP_201_CREATED)

	def test_registration_error(self) -> None:
		''' test to check if route responses with an error '''
		# register with incorrect data
		res = self.client.post(self.url, data=self.incorrect_data)

		# assert status code of the registration response to be 400
		self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

	def test_register_user_with_same_username(self) -> None:
		''' check if api returns a status code of 400 when a user with same email exists already '''
		# register first user
		first_res = self.client.post(self.url, data=self.data)
		# register second user with same data
		second_res = self.client.post(self.url, data=self.data)

		# assert if response of registering second user is 400
		self.assertEqual(second_res.status_code, status.HTTP_400_BAD_REQUEST)
