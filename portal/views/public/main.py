from django.http import HttpResponseRedirect
from django.shortcuts import render

def mainview(request):
    return HttpResponseRedirect('/dashboard')

def dashboard(request):
	return render(request, 'public/dashboard.html')


class Car(object):

	def __init__(self, name, color):
		self.name = name
		self.color = color
		


def home(request):
	if request.method == 'POST':
		email = request.POST.get('email')
		return render(request, 'public/home.html', {'email': email})




	elif request.method == 'GET':
		cars = [Car('bmw', '#848484'), Car('lambo', '#FFFF00')]
		return render(request, 'public/home.html', {'cars': cars})