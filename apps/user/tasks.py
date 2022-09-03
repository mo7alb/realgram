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
	
	previos_profile_img = profile.img.path
	profile_image = img.open(profile.img)

	x_factor = profile_image.size[0] / 550

	profile_img = profile_image.resize((550, int(profile_image.size[1]/x_factor)))
	file_name = "/avatar/{}_avatar.jpeg".format(str(profile.pk))

	byte_array = io.BytesIO()
	profile_img.save(byte_array, format="jpeg")

	file = SimpleUploadedFile(file_name, byte_array.getvalue())

	profile.img = file
	profile.save()

	if os.path.exists(previos_profile_img):
		os.remove(previos_profile_img)