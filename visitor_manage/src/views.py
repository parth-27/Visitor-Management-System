from __future__ import unicode_literals

from django.shortcuts import render,redirect, get_object_or_404
from .models import *
# Create your views here.
def index(request):
    return render(request , 'src/index.html')

def userLogin(request):
    return render(request,'src/userLogin.html')


