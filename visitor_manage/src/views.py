from __future__ import unicode_literals

from django.shortcuts import render,redirect, get_object_or_404
from .models import *
from django.contrib.auth.forms import UserCreationForm
# Create your views here.
def index(request):
    return render(request , 'src/index.html')

def userLogin(request):
    form = UserCreationForm()
    return render(request,'src/userLogin.html',{"form":form})


