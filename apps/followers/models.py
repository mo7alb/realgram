from django.db import models
from apps.user.models import Profile

class Follow(models.Model):
	''' model for a profile to follow another profile '''
	profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='follower')
	follows =  models.ForeignKey(Profile, on_delete=models.CASCADE)

	def __str__(self) -> str:
		return '{} follows {}'.format(self.profile, self.follows)