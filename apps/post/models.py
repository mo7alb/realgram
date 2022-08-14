from django.db import models
from apps.user.models import Profile

class Post(models.Model):
	title = models.CharField(max_length=100)
	caption = models.CharField(
		max_length=100, 
		blank=True, 
		null=True
	)
	body = models.CharField(
		max_length=500, 
		blank=True, 
		null=True
	)
	img = models.ImageField(blank=True)
	user = models.ForeignKey(
		Profile,
		on_delete=models.CASCADE
	)
	# saves the date time once Comment is created
	created_at = models.DateField(null=False, auto_now_add=True, blank=False)
	# saves the date time every time Comment is udpated
	updated_at = models.DateField(null=False, auto_now=True, blank=False)

	def __str__(self) -> str:
		return self.title

class LikePost(models.Model):
	# liking requires a user
	user = models.OneToOneField(Profile, on_delete=models.CASCADE)
	# liking requires a post
	post = models.OneToOneField(Post, on_delete=models.CASCADE)
	