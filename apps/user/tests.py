import json

from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from apps.user.models import *
from apps.user.serializers import *

class RegistrationTestCase(APITestCase):
	''' test if a new user can register '''
	url = ''
	data = None
	incorrect_data = None
	
	def setUp(self) -> None:
		''' set up variables to be used in the tests '''
		self.url = '/api/profile/register/'
		self.incorrect_data = {
			'username': 'johndoe',
			'first_name': 'john'
		}
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
		res = self.client.post(self.url, data=self.data)

		self.assertEqual(res.status_code, status.HTTP_201_CREATED)

	def test_registration_response_data(self) -> None:
		''' test to check if correct data is returned when a user is registered '''
		res = self.client.post(self.url, data=self.data)
		res_data = res.json()
		self.assertEqual(res_data['profile']['username'], 'cha')

	def test_registration_error(self) -> None:
		''' test to check if route responses with an error '''
		res = self.client.post(self.url, data=self.incorrect_data)

		self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

	def test_register_user_with_same_username(self):
		''' check if api returns a status code of 400 when a user with same username exists already '''
		first_res = self.client.post(self.url, data=self.data)
		second_res = self.client.post(self.url, data=self.data)
		self.assertEqual(second_res.status_code, status.HTTP_400_BAD_REQUEST)

	def test_register_user_with_same_username(self):
		''' check if api returns a status code of 400 when a user with same email exists already '''
		first_res = self.client.post(self.url, data=self.data)
		second_res = self.client.post(self.url, data={
			'username': 'chalie',
			'email': 'cha@lie.com',
			'first_name': 'charlie',
			'last_name': 'doe',
			'password': 'super secret',
		})
		self.assertEqual(second_res.status_code, status.HTTP_400_BAD_REQUEST)

class AuthViewSetTestCase(APITestCase):
	login_url:str = ''
	logout_url:str = ''
	data = None
	incorrect_data = None
	incomplete_data = None

	def setUp(self) -> None:
		''' create a profile which is to be used while testing the api routes '''
		# set up the urls
		self.login_url = '/api/profile/authenticate/'
		self.logout_url = '/api/profile/logout/'
		# create good, incomplete and incorrect data
		self.data = {
			'username': 'johndoe',
			'password': 'super secret'
		}
		self.incorrect_data = {
			'username': 'johndoe1',
			'password': 'super secret1'
		}
		self.incomplete_data = { 'username': 'johndoe' }
		# create a profile 
		self.profile = Profile.objects.create(
			bio="cool guy", 
			user=User.objects.create(
				username="johndoe",
				first_name="john",
				last_name="johndoe",
				email="johndoe@somemail.com",
				password=make_password('super secret')
			)
		)

	def tearDown(self) -> None:
		''' clear all tables once all tests are done '''
		Profile.objects.all().delete()
		User.objects.all().delete()

	def test_user_login(self) -> None:
		''' route to check if user is authenticate and returns status of 200 with correct credentail '''
		res = self.client.post(self.login_url, data=self.data)

		self.assertEqual(res.status_code, status.HTTP_200_OK)

	def test_user_login_with_incorrect_data(self) -> None:
		''' test if api returns status code of 404 when incorrect data is passed to it '''
		res = self.client.post(self.login_url, data=self.incorrect_data)

		self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

	def test_user_login_with_incomplete_data(self) -> None:
		''' test if api returns status code of 400 when incomplete data is passed to it '''
		res = self.client.post(self.login_url, data=self.incomplete_data)

		self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
