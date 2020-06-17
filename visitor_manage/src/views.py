from __future__ import unicode_literals

from django.shortcuts import render,redirect, get_object_or_404
from .models import *
from django.contrib import auth
from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm
# Create your views here.
def index(request):
    return render(request , 'src/index.html')

def userLogin(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(username)
        try:
            user_admin_obj = User.objects.get(username=username)
        except:
            user_admin_obj = None
        # user_admin_obj = UserAdmin.objects.get(username=username)
        if user_admin_obj is None:
            errors = "Username you entered doesn't exist"
            return render(request, "src/userLogin.html", {"error": errors})
        elif not user_admin_obj.password == password:
            errors = "Username and password didn't match"
            return render(request, "src/userLogin.html", {"error": errors})
        return render(request, "src/userDash.html")
    return render(request, "src/userLogin.html")
    
def userRegister(request):
    if request.method =='POST':
        username=request.POST.get('username')
        name=request.POST.get('name')
        password=request.POST.get('password')
        mail=request.POST.get('mail')
        contact=request.POST.get('contact')
        gender=request.POST.get('gender')
        photo=request.POST.get('photo')
        print(username, name,password,mail,contact)
        user = User(username=username, name=name, password=password, mail=mail, contact=contact, gender=gender, photo=photo)
        try: 
            user.save()
            return render(request,'src/userLogin.html')
        except Exception as e:
            print(e)
            return render(request,'src/userRegister.html')

    return render(request,'src/userRegister.html')

def gatepass(request):
    if request.method =='POST':
        username=request.POST.get('username')
        name=request.POST.get('name')
        password=request.POST.get('password')
        mail=request.POST.get('mail')
        contact=request.POST.get('contact')
        gender=request.POST.get('gender')
        photo=request.POST.get('photo')
        #print(username, name,password,mail,contact)
        user = User(username=username, name=name, password=password, mail=mail, contact=contact, gender=gender, photo=photo)
        try: 
            user.save()
            return render(request,'src/userLogin.html')
        except Exception as e:
            print(e)
            return render(request,'src/userRegister.html')

    return render(request,'src/userRegister.html')


