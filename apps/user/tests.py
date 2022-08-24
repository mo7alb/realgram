import json

from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from apps.user.models import *
from apps.user.serializers import *

class RegistrationTestCase(APITestCase):
	def test_registration(self):
		data = {
			'username': 'cha',
			'email': 'cha@lie.com',
			'first_name': 'charlie',
			'last_name': 'doe',
			'password': 'super secret',
		}

		res = self.client.post('/api/profile/register/', data=data)
		self.assertEqual(res.status_code, status.HTTP_201_CREATED)