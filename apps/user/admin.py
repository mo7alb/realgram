from django.contrib import admin
from .models import Profile

class ProfileAdmin(admin.ModelAdmin):
	model = Profile
	fields = [
		'user',
		'date_of_birth',
		'bio',
		'avatar',
	]

admin.site.register(Profile, ProfileAdmin)