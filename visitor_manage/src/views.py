from __future__ import unicode_literals

from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from django.contrib import auth
from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm
# Create your views here.


def index(request):
    return render(request, 'src/index.html')


def userLogin(request):
    if request.method == 'POST':
        form = AuthenticationForm(request.POST)

        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)

        print(username)
        print(user)
        return render(request, 'src/userRegister.html')
    else:
        form = AuthenticationForm()
    return render(request, 'src/userLogin.html')


def userRegister(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        name = request.POST.get('name')
        password = request.POST.get('password')
        mail = request.POST.get('mail')
        contact = request.POST.get('contact')
        gender = request.POST.get('gender')
        photo = request.POST.get('photo')
    return render(request, 'src/userRegister.html')
