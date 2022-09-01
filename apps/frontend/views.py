from django.shortcuts import render

def index(request):
	''' view to render the single page application '''
	return render(request, 'index.html')