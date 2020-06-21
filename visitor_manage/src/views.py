from __future__ import unicode_literals

from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect
from .models import *
from django.contrib import auth
from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm
from django.core.mail import send_mail
from django.contrib import messages
from django.utils.timezone import utc

import datetime
from datetime import datetime, timedelta , timezone


def sendMail(request):
    send_mail('Sending OTP for Pass Generation', "420 is the otp for your password",
              "",
              [''],  # "list of recpetenets",
              fail_silently=False
              )
    return render(request, 'src/forgotPassword.html')


userid = -1
gate_id = -1


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
            visitor_obj = Visitor.objects.all.filter(userId=user_admin_obj.id, checkin=None )
        except:
            visitor_obj = None
        obj = -1
        # print(visitor_obj.userId)
        if visitor_obj is None or len(visitor_obj)==0:
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
        'typo': type,
        'src': "https://img.icons8.com/ios-glyphs/2x/caspar-king-magician.png",
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

def statistics(request):
    dayVisitor=[0]*10
    day=['2000-03-12']*10
    c=0
    while(c<10):
        day[c]=datetime.strftime(datetime.now() - timedelta(c), '%Y-%m-%d')
        visitor=Visitor.objects.all().filter(visitDate=day[c] ).exclude(checkout=None)
        dayVisitor[c]= len(visitor)
        c+=1
    context={
        'dayVisitor': dayVisitor,
        'day': day,
    }
    #print(datetime.strftime(datetime.now() - timedelta(30), '%Y-%m-%d'))
    return render(request, 'src/statistics.html' , context)

def adminEdit(request, pk):
    admin_obj = Admin.objects.get(gate=pk)
    print(admin_obj)
    context = {
        'admin_obj': admin_obj,
    }
    if request.method == 'POST':
        #gate = request.POST.get('gate')
        username = request.POST.get('username')
        name = request.POST.get('name')
        mail = request.POST.get('mail')
        contact = request.POST.get('contact')
        gender = request.POST.get('gender')

        admin_obj.username = username
        admin_obj.name = name
        admin_obj.mail = mail
        admin_obj.contact = contact
        admin_obj.gender = gender

        #admin = Admin( username=username, name=name,password=password, mail=mail, contact=contact, gender=gender)
        try:
            admin_obj.save()
            return HttpResponseRedirect('/adminLogin/superAdminDash/')
            # return render(request, 'src/superAdminDash.html')
        except Exception as e:
            print(e)
            return render(request, 'src/adminEdit.html', context)

    return render(request, 'src/adminEdit.html', context)


def adminDelete(request, pk):
    admin_obj = Admin.objects.get(gate=pk).delete()

    return HttpResponseRedirect('/adminLogin/superAdminDash/')


def gateAdminLogin(request):
    username = "GateId"
    type = "number"
    context = {
        'username': username,
        'typo': type,
        'src': "https://img.icons8.com/ios-filled/2x/front-gate-closed.png",
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
       
        #messages.info(request, 'Your password has been changed successfully!')
        return HttpResponseRedirect('gateAdminDash/')
        # return render(request,'src/superAdminDash.html')

    return render(request, "src/adminLogin.html", context)


def gateAdminDash(request ):
    visitor_obj = Visitor.objects.all().filter(visitDate= datetime.now().date(), checkout=None , gateId= gate_id).exclude(checkin=None)
    l=[]
    for i in range(len(visitor_obj)):
        if visitor_obj[i].visiting_hour!="More Than 3":
            now =datetime.utcnow().replace(tzinfo=utc)
            diff= visitor_obj[i].checkin - now
            hour=5.5-float(diff.total_seconds()/3600)
            if visitor_obj[i].visiting_hour=="1":
                if hour>1:
                    user_obj= (visitor_obj[i].userId)
                    l.append(user_obj.name)
            if visitor_obj[i].visiting_hour=="2":
                if hour>2:
                    user_obj=  (visitor_obj[i].userId)
                    l.append(user_obj.name)
            if visitor_obj[i].visiting_hour=="3":
                if hour>3:
                    user_obj=  (visitor_obj[i].userId)
                    l.append(user_obj.name)
    #print(l)
    context={
        'messages':l,
    }
    if request.method == 'POST':
        name = request.POST.get('name')
        mail = request.POST.get('mail')
        contact = request.POST.get('contact')
        gender = request.POST.get('gender')
        photo = request.POST.get('photo')
        gateId = gate_id
        visit_gate = Admin.objects.get(gate=gateId)
        visitDate = datetime.datetime.now().date()
        visiting_hour = request.POST.get('visiting_hour')
        reason = request.POST.get('reason')
        checkin = datetime.datetime.now()
        user = TemporaryUser(name=name, mail=mail, contact=contact, gender=gender, photo=photo, gateId=visit_gate,
                             checkin=checkin, visitDate=visitDate, visiting_hour=visiting_hour, reason=reason)
        try:
            user.save()
            return render(request, 'src/index.html')
        except Exception as e:
            print(e)
            return render(request, 'src/gateAdminDashhtml', context)

    return render(request, 'src/gateAdminDash.html', context)


def makeCheckIn(request):
    obj = -1
    try:
        visitor_obj = Visitor.objects.all().filter( checkin=None, gateId=gate_id ,visitDate=datetime.now().date()) 
    except:
        visitor_obj = None
    #print(len(visitor_obj))
    #print('z')
    if visitor_obj is None or len(visitor_obj)==0:
        context = {
            'obj': obj,
        }
        return render(request, 'src/makeCheckIn.html', context)
    else:
        l=[0]*len(visitor_obj)

        for i in range(len(visitor_obj)):
            x=visitor_obj[i].userId
            l[i]=x
        obj=1
        context={
            'obj':obj,
            'visitor_obj': visitor_obj,
            'x':l,
            'len':len(visitor_obj),
        }
        return render(request, 'src/makeCheckIn.html',context)

def checkInVisitor(request, pk):
    print(pk)
    visitor_obj=Visitor.objects.get(id=pk , checkin=None, visitDate=datetime.now().date() )
    visitor_obj.checkin=datetime.now()
    try:
        visitor_obj.save()

    except Exception as e:
        print(e)
    return HttpResponseRedirect('/makeCheckIn/')

def makeCheckOut(request):
    obj=-1
    try:
        visitor_obj = Visitor.objects.all().filter( checkout=None , gateId=gate_id ,visitDate=datetime.now().date()).exclude(checkin=None)
    except:
        visitor_obj = None

    if visitor_obj is None or len(visitor_obj)==0:
        context={
            'obj':obj,
        }
        return render(request, 'src/makeCheckOut.html',context)
    else:
        l=[0]*len(visitor_obj)

        for i in range(len(visitor_obj)):
            x=visitor_obj[i].userId
            l[i]=x
        obj=1
        context={
            'obj':obj,
            'visitor_obj': visitor_obj,
            'x':l,
            'len':len(visitor_obj),
        }
        return render(request, 'src/makeCheckOut.html', context)

def checkOutVisitor(request, pk):
    print(pk)
    visitor_obj=Visitor.objects.get(id=pk , checkout=None, visitDate=datetime.now().date(),)
    visitor_obj.checkout=datetime.datetime.now()
    try:
        visitor_obj.save()

    except Exception as e:
        print(e)
    return HttpResponseRedirect('/makeCheckOut/')

def checkOutDone(request):
    obj=-1
    try:
        visitor_obj = Visitor.objects.all().filter(visitDate=datetime.now().date(), gateId=gate_id ).exclude( checkout=None)
        print(visitor_obj)
    except:
        visitor_obj = None

    if visitor_obj is None or len(visitor_obj)==0:
        context={
            'obj':obj,
        }
        return render(request, 'src/checkOutDone.html',context)
    else:
        l=[0]*len(visitor_obj)

        for i in range(len(visitor_obj)):
            x=visitor_obj[i].userId
            l[i]=x
        obj=1
        context={
            'obj':obj,
            'visitor_obj': visitor_obj,
            'x':l,
            'len':len(visitor_obj),
        }
        return render(request, 'src/checkOutDone.html', context)