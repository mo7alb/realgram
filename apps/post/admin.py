from typing import Sequence
from django.contrib import admin
from apps.post.models import Post, LikePost

class PostAdmin(admin.ModelAdmin):
	fields: Sequence[str] = [
		'title',
		'caption',
		'body',
		'img',
		'profile'
	]

	class Meta:
		model = Post

admin.site.register(Post, PostAdmin)
admin.site.register(LikePost)
