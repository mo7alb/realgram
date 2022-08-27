from typing import Sequence
from django.contrib import admin
from apps.post.models import Post, LikePost
from apps.user.models import Profile
class ProfileInline(admin.TabularInline):
	model = Profile

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
