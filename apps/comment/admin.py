from django.contrib import admin
from .models import Comment, LikeComment

admin.site.register(Comment)
admin.site.register(LikeComment)