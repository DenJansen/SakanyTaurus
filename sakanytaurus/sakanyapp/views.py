from django.shortcuts import render, reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

# Create your views here.

# def register(request):
#     return render(request, 'users/register.html')
#
# def register_user(request):
#     username = request.POST['username']
#     email = request.POST['email']
#     password = request.POST['password']
#     user = User.objects.create_user(username, email, password)
#     login(request, user)
#     return HttpResponseRedirect(reverse(''))

def login_page  (request):
    return render(request, 'sakanyapp/login.html')

def registration (request):
    return HttpResponse("Success!")

@login_required
def index(request):
    return render(request, ('sakanyapp/index.html'))
