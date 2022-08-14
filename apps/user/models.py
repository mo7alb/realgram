from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
	user = models.OneToOneField(
		User, 
		null=False, 
		on_delete=models.CASCADE
	)
	date_of_birth = models.DateField()
	bio = models.TextField(max_length=256, null=True)
	avatar = models.ImageField()

	def __str__(self) -> str:
		return self.user.username