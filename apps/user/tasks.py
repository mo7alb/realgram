from django.core.files.uploadedfile import SimpleUploadedFile
from celery import shared_task
from .models import Profile
from PIL import Image as img
import io


@ shared_task
def make_avatar(pk):
	''' scale the size of the avatar and upload it '''
	profile = Profile.objects.get(pk=pk)
	
	image = img.open(profile.avatar)
	x_factor = image.size[0] / 260

	avatar = image.resize((260, int(image.size[1]/x_factor)))
	file_name = "/avatars/{}_avatar.jpeg".format(str(profile.pk))

	byte_array = io.BytesIO()
	avatar.save(byte_array, format="jpeg")

	file = SimpleUploadedFile(file_name, byte_array.getvalue())

	profile.avatar = file
	profile.save()