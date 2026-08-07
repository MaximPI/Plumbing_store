from django.shortcuts import render, HttpResponseRedirect
from users.forms import UserLoginForm
from django.contrib import auth
from django.urls import reverse

def login(request):
	if request.method == 'POST':
		form = UserLoginForm(data=request.POST)
		if form.is_valid():
			username = request.POST['username']
			password = request.POST['password']
			user = auth.authenticate(username=username, password=password)
			if user and user.is_active:
				auth.login(request, user)
				return HttpResponseRedirect(reverse('home'))
	else:
		form = UserLoginForm()

	context = {
		"form": form
	}
	return render(request, 'users/login.html', context)

def profile(request):
	return render(request, 'users/profile.html')

def register(request):
	return render(request, 'users/register.html')