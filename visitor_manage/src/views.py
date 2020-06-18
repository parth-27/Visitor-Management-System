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
        
        login(user_admin_obj.id)
        #print(userid)
        try:
            visitor_obj= Visitor.objects.get(userId = user_admin_obj.id , checkin =None )
        except:
            visitor_obj=None
        obj=-1
        #print(visitor_obj.userId)
        if visitor_obj is None:
            context = {
                'username':username,
                'obj':obj,
            }
            return render(request,'src/userDash.html',context)
        else:
            obj=1
            context = {
                'username':username,
                'obj': obj,
                'visiter_obj':visitor_obj,
                'user_admin_obj':user_admin_obj,
            }
            
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
        #print(gender)
        photo=request.POST.get('photo')
        #print(username, name,password,mail,contact)
        user = User(username=username, name=name, password=password, mail=mail, contact=contact, gender=gender, photo=photo)
        try: 
            obj=-1
            user.save()
            context = {
                'username':username,
                'obj':obj,
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
        visiting_hour = request.POST.get('visiting_hour')
        reason = request.POST.get('reason')
        visit_gate = Admin.objects.get(gate=gateId)
        user_id = User.objects.get(id=userId)
        #print(visit_gate)
        #print(username, name,password,mail,contact)
        visitor = Visitor(gateId=visit_gate, userId=user_id, visitDate=visitDate, visiting_hour=visiting_hour, reason=reason)
        try: 
            visitor.save()
            obj=1
            context = {
                'username':user_id.username,
                'obj': obj,
                'visiter_obj':visitor,
                'user_admin_obj':user_id,
            }
            
            return render(request,'src/userDash.html', context)
        except Exception as e:
            print(e)
            return render(request,'src/gatepass.html',context)

    return render(request,'src/gatepass.html', context)


