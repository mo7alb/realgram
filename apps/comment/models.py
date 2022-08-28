from django.db import models
from apps.user.models import Profile
from apps.post.models import Post

class Comment(models.Model):
	message = models.CharField(
		max_length=200,
		null=False, 
		blank=False
	)
	profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
	post = models.ForeignKey(Post, on_delete=models.CASCADE)
	# saves the date time once Comment is created
	created_at = models.DateField(null=False, auto_now_add=True)
	# saves the date time every time Comment is udpated
	updated_at = models.DateField(null=False, auto_now=True)

	def __str__(self) -> str:
		return self.message

class LikeComment(models.Model):
	profile = models.ForeignKey(Profile,on_delete=models.CASCADE)
	comment = models.ForeignKey(Comment,on_delete=models.CASCADE)
