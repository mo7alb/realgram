from django.db import models

from apps.user.models import Profile

class Room(models.Model):
	slug = models.SlugField(primary_key=True, unique=True, editable=False, blank=True)

	first_profile = models.ForeignKey(Profile,on_delete=models.CASCADE, related_name='first_profile')
	second_profile = models.ForeignKey(Profile,on_delete=models.CASCADE)

	def __str__(self) -> str:
		return self.slug


class Message(models.Model):
	room = models.ForeignKey(Room, on_delete=models.CASCADE)
	reciever = models.ForeignKey(Profile, on_delete=models.CASCADE)
	sent_at = models.DateTimeField(auto_now_add=True)
	message = models.TextField(null=False, blank=False)

	def __str__(self) -> str:
		return self.message