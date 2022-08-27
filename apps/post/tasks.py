from django.core.files.uploadedfile import SimpleUploadedFile
from celery import shared_task
from apps.post.models import Post
from PIL import Image as img
import io

@ shared_task
def make_post_img(pk:int):
	''' scale the size of the img and upload it '''
	post = Post.objects.get(pk=pk)
	
	post_image = img.open(post.img)
	x_factor = post_image.size[0] / 550

	img = post_image.resize((550, int(post_image.size[1]/x_factor)))
	file_name = "/posts/{}_img.jpeg".format(str(post.pk))

	byte_array = io.BytesIO()
	img.save(byte_array, format="jpeg")

	file = SimpleUploadedFile(file_name, byte_array.getvalue())

	post.img = file
	post.save()