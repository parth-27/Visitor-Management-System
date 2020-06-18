from __future__ import unicode_literals

from django.shortcuts import render,redirect, get_object_or_404
from .models import *
from django.contrib import auth
from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm
# Create your views here.
userid=-1

def index(request):
    return render(request , 'src/index.html')

def login(id):
    global userid
    userid=id

def logout():
    global userid
    userid=-1

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
        context = {
            'username':username,
        }
        login(user_admin_obj.id)
        print(userid)
        return render(request,'src/userDash.html',context)
    return render(request, "src/userLogin.html")
    
def userRegister(request):
    if request.method =='POST':
        username=request.POST.get('username')
        name=request.POST.get('name')
        password=request.POST.get('password')
        mail=request.POST.get('mail')
        contact=request.POST.get('contact')
        gender=request.POST.get('gender')
        print(gender)
        photo=request.POST.get('photo')
        #print(username, name,password,mail,contact)
        user = User(username=username, name=name, password=password, mail=mail, contact=contact, gender=gender, photo=photo)
        try: 
            user.save()
            context = {
                'username':username,
            }
            login(user.id)
            return render(request,'src/userDash.html',context)
        except Exception as e:
            print(e)
            return render(request,'src/userRegister.html')

    return render(request,'src/userRegister.html')

def gatepass(request):
    gateid=Admin.objects.all()
    #print(gateid)
    context = {
            'gateid':gateid,
    }
    if request.method =='POST':
        gateId = request.POST.get('gateId')
        userId =userid
        visitDate = request.POST.get('visitDate')
        visiting_hour = models.CharField(max_length=20, default=1)
        reason = request.POST.get('reason')
        visit_gate = Admin.objects.get(gate=gateId)
        user_id = User.objects.get(id=userId)
        #print(visit_gate)
        #print(username, name,password,mail,contact)
        visitor = Visitor(gateId=visit_gate, userId=user_id, visitDate=visitDate, visiting_hour=visiting_hour, reason=reason)
        try: 
            visitor.save()
            return render(request,'src/userDash.html')
        except Exception as e:
            print(e)
            return render(request,'src/gatepass.html',context)

    return render(request,'src/gatepass.html', context)


