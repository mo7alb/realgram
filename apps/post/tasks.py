import io
import os

from celery import shared_task
from django.core.files.uploadedfile import SimpleUploadedFile
from PIL import Image as img

from apps.post.models import Post


@ shared_task
def make_post_img(pk:int):
	''' scale the size of the img and upload it '''
	post = Post.objects.get(pk=pk)
	
	previos_post_img = post.img.path
	post_image = img.open(post.img)

	x_factor = post_image.size[0] / 550

	post_img = post_image.resize((550, int(post_image.size[1]/x_factor)))
	file_name = "/posts/{}_img.jpeg".format(str(post.pk))

	byte_array = io.BytesIO()
	post_img.save(byte_array, format="jpeg")

	file = SimpleUploadedFile(file_name, byte_array.getvalue())

	post.img = file
	post.save()

	if os.path.exists(previos_post_img):
		os.remove(previos_post_img)
	