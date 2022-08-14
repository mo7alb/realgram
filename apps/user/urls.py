from django.urls import path
from .api import *

urlpatterns = [
	# path to authenticate user
	path('authenticate/'),
	# path to register new user
	path('register/'),
	# path to return user profile
	path('profile/'),
]