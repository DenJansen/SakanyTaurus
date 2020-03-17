from django.shortcuts import render, reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from . import secrets

import json

# Create your views here.
#
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

def login_page(request):
    message = request.GET.get('message', '')
    next = request.GET.get('next', '')
    context = {
        'next': next,
        'message': message
    }
    return render(request, 'sakanyapp/login.html', context)

def user_login (request):
    next = request.POST['next']
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        if next != '':
            return HttpResponseRedirect(next)
        return HttpResponseRedirect(reverse('sakanyapp:index'))
    if next == '':
        return HttpResponseRedirect(reverse('sakanyapp:login') + '?message=failure')
    return HttpResponseRedirect(reverse('sakanyapp:login') + '?message=failure&next='+next)

@login_required
def index(request):
    context = {
        'mapapi': secrets.mapapi
    }
    return render(request, 'sakanyapp/index.html', context)
