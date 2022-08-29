
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from apps.user.models import *
from apps.user.serializers import *


class AuthViewSetTestCase(APITestCase):
	login_url:str = ''
	logout_url:str = ''
	data = None
	incorrect_data = None
	incomplete_data = None

	def setUp(self) -> None:
		''' create a profile which is to be used while testing the api routes '''
		# login and log out urls
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
		# a profile to be stored in db
		Profile.objects.create(
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

	def test_user_logout(self) -> None:
		''' test if the user can successfully logout once logged in '''
		log_res = self.client.post(self.login_url, data=self.data)
		token = log_res.json()['token']

		header = {'HTTP_AUTHORIZATION': 'Token {}'.format(token)}

		res = self.client.post(
			self.logout_url, 
			data={},
			**header
		)

		self.assertEqual(res.status_code, status.HTTP_200_OK)
