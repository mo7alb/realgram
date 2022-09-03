from django.db import models

from apps.user.models import Profile

class Message(models.Model):
	''' a model to store messages sent to other users '''
	sender = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='sender')
	reciever = models.ForeignKey(Profile, on_delete=models.CASCADE)
	# time at which the message is sent 
	sent_at = models.DateTimeField(auto_now_add=True)
	# the message sent
	message = models.CharField(max_length=300)

	def __str__(self) -> str:
		''' return message if the model is accessed as a string '''
		return self.message
