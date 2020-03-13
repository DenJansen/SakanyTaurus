from django.shortcuts import render, reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

# Create your views here.

def index(request):
    context = {
        'message': 'Hello World!'
    }
    return render(request, reverse('sakanyapp:index'), context)

def register(request):
    return render(request, 'users/register.html')

def register_user(request):
    username = request.POST['username']
    email = request.POST['email']
    password = request.POST['password']
    user = User.objects.create_user(username, email, password)
    login(request, user)

    return HttpResponseRedirect(reverse(''))
