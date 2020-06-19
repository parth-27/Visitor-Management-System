from __future__ import unicode_literals

from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect
from .models import *
from django.contrib import auth
from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm
from django.core.mail import send_mail

import datetime

def sendMail(request):
    send_mail('Sending OTP for Pass Generation', "420 is the otp for your password",
              "",
              [''],  # "list of recpetenets",
              fail_silently=False
              )
    return render(request, 'src/forgotPassword.html')


userid = -1
gate_id=-1

def index(request):
    return render(request, 'src/index.html')


def login(id):
    global userid
    userid = id

def gateLogin(id):
    global gate_id
    gate_id = id


def logout():
    global userid
    userid = -1


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
        # print(userid)
        try:
            visitor_obj = Visitor.objects.get(
                userId=user_admin_obj.id, checkin=None)
        except:
            visitor_obj = None
        obj = -1
        # print(visitor_obj.userId)
        if visitor_obj is None:
            context = {
                'username': username,
                'obj': obj,
            }
            return render(request, 'src/userDash.html', context)
        else:
            obj = 1
            context = {
                'username': username,
                'obj': obj,
                'visiter_obj': visitor_obj,
                'user_admin_obj': user_admin_obj,
            }

            return render(request, 'src/userDash.html', context)

    return render(request, "src/userLogin.html")

def userRegister(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        name = request.POST.get('name')
        password = request.POST.get('password')
        mail = request.POST.get('mail')
        contact = request.POST.get('contact')
        gender = request.POST.get('gender')
        # print(gender)
        photo = request.POST.get('photo')
        #print(username, name,password,mail,contact)
        user = User(username=username, name=name, password=password,
                    mail=mail, contact=contact, gender=gender, photo=photo)
        try:
            obj = -1
            user.save()
            context = {
                'username': username,
                'obj': obj,
            }
            login(user.id)
            return render(request, 'src/userDash.html', context)
        except Exception as e:
            print(e)
            return render(request, 'src/userRegister.html')

    return render(request, 'src/userRegister.html')


def gatepass(request):
    gateid = Admin.objects.all()
    # print(gateid)
    context = {
        'gateid': gateid,
    }
    if request.method == 'POST':
        gateId = request.POST.get('gateId')
        userId = userid
        visitDate = request.POST.get('visitDate')
        visiting_hour = request.POST.get('visiting_hour')
        reason = request.POST.get('reason')
        visit_gate = Admin.objects.get(gate=gateId)
        user_id = User.objects.get(id=userId)
        # print(visit_gate)
        #print(username, name,password,mail,contact)
        visitor = Visitor(gateId=visit_gate, userId=user_id,
                          visitDate=visitDate, visiting_hour=visiting_hour, reason=reason)
        try:
            visitor.save()
            obj = 1
            context = {
                'username': user_id.username,
                'obj': obj,
                'visiter_obj': visitor,
                'user_admin_obj': user_id,
            }

            return render(request, 'src/userDash.html', context)
        except Exception as e:
            print(e)
            return render(request, 'src/gatepass.html', context)

    return render(request, 'src/gatepass.html', context)

def adminLogin(request):
    username = "username"
    type = "text"
    context = {
        'username': username,
        'typo': type
    }
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(username)
        try:
            user_admin_obj = SuperAdmin.objects.get(username=username)
        except:
            user_admin_obj = None
        # user_admin_obj = UserAdmin.objects.get(username=username)
        if user_admin_obj is None:
            errors = "Username you entered doesn't exist"
            return render(request, "src/adminLogin.html", {"error": errors}, context)
        elif not user_admin_obj.password == password:
            errors = "Username and password didn't match"
            return render(request, "src/adminLogin.html", {"error": errors}, context)

        return HttpResponseRedirect('superAdminDash/')
        # return render(request,'src/superAdminDash.html')

    return render(request, "src/adminLogin.html", context)

def superAdminDash(request):
    admin_obj = Admin.objects.all()
    context = {
        'admin_obj': admin_obj,
    }
    if request.method == 'POST':
        gate = request.POST.get('gate')
        username = request.POST.get('username')
        name = request.POST.get('name')
        password = request.POST.get('password')
        mail = request.POST.get('mail')
        contact = request.POST.get('contact')
        gender = request.POST.get('gender')

        admin = Admin(gate=gate, username=username, name=name,
                      password=password, mail=mail, contact=contact, gender=gender)
        try:
            admin.save()
            admin_obj = Admin.objects.all()
            context = {
                'admin_obj': admin_obj,
            }
            return render(request, 'src/superAdminDash.html', context)
        except Exception as e:
            print(e)
            return render(request, 'src/superAdminDash.html', context)

    return render(request, 'src/superAdminDash.html', context)
def gateAdminLogin(request):
    username = "GateId"
    type = "number"
    context = {
        'username': username,
        'typo': type
    }
    if request.method == "POST":
        gateId = (request.POST.get('username'))
        password = request.POST.get('password')
        print(username)
        try:
            user_admin_obj = Admin.objects.get(gate=gateId)
        except:
            user_admin_obj = None
        # user_admin_obj = UserAdmin.objects.get(username=username)
        if user_admin_obj is None:
            errors = "Gate ID you entered doesn't exist"
            return render(request, "src/adminLogin.html", {"error": errors}, context)
        elif not user_admin_obj.password == password:
            errors = "Gate Id and password didn't match"
            return render(request, "src/adminLogin.html", {"error": errors}, context)

        gateLogin(gateId)
        return HttpResponseRedirect('gateAdminDash/')
        # return render(request,'src/superAdminDash.html')

    return render(request, "src/adminLogin.html", context)


def gateAdminDash(request):

    if request.method == 'POST':
        name = request.POST.get('name')
        mail = request.POST.get('mail')
        contact = request.POST.get('contact')
        gender = request.POST.get('gender')
        photo = request.POST.get('photo')
        gateId= gate_id
        visit_gate = Admin.objects.get(gate=gateId)
        visitDate= datetime.datetime.now().date()
        visiting_hour= request.POST.get('visiting_hour')
        reason= request.POST.get('reason')
        checkin = datetime.datetime.now()
        user = TemporaryUser(name=name,mail=mail, contact=contact, gender=gender, photo=photo, gateId=visit_gate ,checkin=checkin, visitDate=visitDate,visiting_hour=visiting_hour, reason=reason)
        try:
            user.save()
            return render(request, 'src/index.html')
        except Exception as e:
            print(e)
            return render(request, 'src/gateAdminDashhtml')

    return render(request, 'src/gateAdminDash.html')



def makeCheckIn(request):
    obj=-1
    try:
        visitor_obj = Visitor.objects.all().filter( checkin=None, visitDate=datetime.datetime.now().date()) 
    except:
        visitor_obj = None

    if visitor_obj is None:
        context={
            'obj':obj,
        }
        return render(request, 'src/makeCheckIn.html',context)
    else:
        #user_obj = User.objects.get.all(id=visiter_obj)
        #print(user_obj)
        obj=1
        context={
            'obj':obj,
            'visitor_obj': visitor_obj,
            #'user_obj': user_obj,
        }
        return render(request, 'src/makeCheckIn.html',context)

    
    



