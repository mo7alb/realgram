import factory

from apps.post.models import *
from apps.user.models import Profile
from django.contrib.auth.models import User

class UserFactory(factory.django.DjangoModelFactory):
	username = "doey"
	email = "doey@doey.com"
	first_name = "doey"
	last_name = "doey"

	class Meta:
		model = User

class ProfileFactory(factory.django.DjangoModelFactory):
	user = factory.SubFactory(UserFactory)
	bio = "doey is a doey"

	class Meta:
		model = Profile

class PostFactory(factory.django.DjangoModelFactory):
	title = "Welcome to this platform"
	caption = "Welcome to this platform"
	img = "Welcome to this platform"
	created_at = factory.Faker('date_object')
	updated_at = factory.Faker('date_object')
	profile = factory.SubFactory(ProfileFactory)

	class Meta:
		model = Post