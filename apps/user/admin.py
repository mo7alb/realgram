from django.contrib import admin
from .models import Profile

class ProfileAdmin(admin.ModelAdmin):
	model = Profile
	fields = [
		'user',
		'bio',
		'avatar',
	]

admin.site.register(Profile, ProfileAdmin)