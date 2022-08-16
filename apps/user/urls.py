from django.urls import path, include
from .views import NewProfile


urlpatterns = [
	path('api/profile/register/', NewProfile.as_view())
]