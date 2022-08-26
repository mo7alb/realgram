from django.db import models
from apps.user.models import Profile

class Post(models.Model):
	# title for the post
	title = models.CharField(max_length=100)
	# post caption
	caption = models.CharField(max_length=300, blank=True, null=True)
	# content of the post
	body = models.TextField(max_length=700, blank=True, null=True)
	# image related to the post 
	img = models.ImageField(blank=True, null=True, upload_to='posts/')
	# user who posted the post
	profile = models.OneToOneField(Profile, on_delete=models.CASCADE)
	# saves the date time once Comment is created
	created_at = models.DateField(auto_now_add=True)
	# saves the date time every time Comment is udpated
	updated_at = models.DateField(auto_now=True)

	def __str__(self) -> str:
		return "{} - {}".format(self.user, self.title)

class LikePost(models.Model):
	# liking requires a user
	user = models.ForeignKey(Profile, on_delete=models.CASCADE)
	# liking requires a post
	post = models.ForeignKey(Post, on_delete=models.CASCADE)
	