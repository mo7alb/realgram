from django.urls import path
from apps.frontend.views import index

# url patters for the app 
urlpatterns = [
	path('', index, name='index') # point the / route to index view 
]