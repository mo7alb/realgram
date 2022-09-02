import profile
from django.db import models
from apps.user.models import Profile

class Post(models.Model):
	# title for the post
	title = models.CharField(max_length=100, null=False, blank=False)
	# post caption
	caption = models.CharField(max_length=300, blank=True, null=True)
	# content of the post
	body = models.TextField(max_length=700, blank=True, null=True)
	# image related to the post 
	img = models.ImageField(blank=True, null=True, upload_to='posts/')
	# user who posted the post
	profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
	# saves the date time once Comment is created
	created_at = models.DateField(null=True, blank=True, auto_now_add=True)
	# saves the date time every time Comment is udpated
	updated_at = models.DateField(null=True, blank=True, auto_now=True)

	def __str__(self) -> str:
		return "{}".format(self.title)

class LikePost(models.Model):
	# liking requires a user profile
	profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
	# liking requires a post
	post = models.ForeignKey(Post, on_delete=models.CASCADE)

	def __str__(self) -> str:
		return "{} liked {}".format(self.profile, self.post)
	