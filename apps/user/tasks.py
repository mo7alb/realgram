from django.core.files.uploadedfile import SimpleUploadedFile
from celery import shared_task
from apps.user.models import Profile
from PIL import Image as img
import io
import os

@ shared_task
def make_avatar(id):
	''' scale the size of the avatar and upload it '''
	profile = Profile.objects.get(id=id)

	previous_avatar = profile.avatar.path
	
	image = img.open(profile.avatar)
	x_factor = image.size[0] / 260

	avatar = image.resize((260, int(image.size[1]/x_factor)))
	file_name = "/avatars/{}_avatar.jpeg".format(str(profile.id))

	byte_array = io.BytesIO()
	avatar.save(byte_array, format="jpeg")

	file = SimpleUploadedFile(file_name, byte_array.getvalue())

	profile.avatar = file
	profile.save()

	if os.path.exists(previous_avatar):
		os.remove(previous_avatar)