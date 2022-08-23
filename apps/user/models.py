from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
	bio = models.TextField(max_length=256, null=True)
	avatar = models.FileField(blank=True, null=True, upload_to='avatars/')

	def __str__(self) -> str:
		return self.user.username