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
from django.core import mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.utils.dateparse import parse_date
from django.core.serializers.json import DjangoJSONEncoder
import datetime
from datetime import datetime, timedelta, timezone
import json
from django.core.files.storage import FileSystemStorage
import random


userid = -1
gate_id = -1
superAdminId = -1
e_mail = ""
otp_f = 0


def supermail(mail, otp):
    global e_mail
    e_mail = mail
    global otp_f
    otp_f = otp


def login(id):
    global userid
    userid = id


def logout():
    global userid
    userid = -1


def gateLogin(id):
    global gate_id
    gate_id = id


def gateLogout():
    global gate_id
    gate_id = -1


def superLogin(id):
    global superAdminId
    superAdminId = id


def superLogout():
    global superAdminId
    superAdminId = -1


def index(request):
    logout()
    gateLogout()
    superLogout()
    now = datetime.now().date()
    year = now.year
    print(year)

    return render(request, 'src/index.html')


def userLogin(request):
    logout()
    gateLogout()
    superLogout()
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
            error = "Username you entered doesn't exist"
            return render(request, "src/userLogin.html", {"error": error})
        elif not user_admin_obj.password == password:
            errors = "Username and password didn't match"
            return render(request, "src/userLogin.html", {"errors": errors})

        login(user_admin_obj.id)
        try:
            visitor_obj = Visitor.objects.all().filter(
                userId=user_admin_obj.id, checkin=None)
        except:
            visitor_obj = None
        obj = -1
        # print(visitor_obj)
        if visitor_obj is None or len(visitor_obj) == 0:
            context = {
                'username': username,
                'obj': obj,
                'user_admin_obj': user_admin_obj,
            }
            return render(request, 'src/userDash.html', context)
        else:
            obj = 1
            context = {
                'username': username,
                'obj': obj,
                'visiter_obj': visitor_obj[0],
                'user_admin_obj': user_admin_obj,
            }

            return render(request, 'src/userDash.html', context)

    return render(request, "src/userLogin.html")


def userRegister(request):
    logout()
    gateLogout()
    superLogout()
    if request.method == 'POST':
        username = request.POST.get('username')
        name = request.POST.get('name')
        password = request.POST.get('password')
        mail = request.POST.get('mail')
        otp = random.randint(1000, 9999)
        send_mail("Confirmation Mail", "OTP for the User Confirmation is {}".format(otp),
                  "visitormanage10@gmail.com",
                  [mail],
                  fail_silently=False
                  )
        print(mail)
        print(otp)
        supermail(mail, otp)
        contact = request.POST.get('contact')
        gender = request.POST.get('gender')
        # print(gender)
        photo = request.FILES['photo']
        fs = FileSystemStorage()
        fs.save(photo.name, photo)
        #print(username, name,password,mail,contact)
        user = User(username=username, name=name, password=password,
                    mail=mail, contact=contact, gender=gender, photo=photo)
        try:
            obj = -1
            user.save()
            context = {
                'username': username,
                'obj': obj,
                'user_admin_obj': user,
            }
            login(user.id)
            return HttpResponseRedirect('/userRegister/userConfirmation')
            # return render(request, 'src/userDash.html', context)
        except Exception as e:
            print(e)
            errors = "*We found the same username or email id in our data. These should be unique. Try some new"
            context = {
                'errors': errors,
            }
            return render(request, 'src/userRegister.html', context)
    return render(request, 'src/userRegister.html')


def userConfirmation(request):

    print(e_mail)
    print(otp_f)
    if request.method == "POST":
        OTP = int(request.POST.get('otpConfirm'))

        if OTP == otp_f:
            return render(request, 'src/userDash.html')
        else:
            User.objects.get(id=userid).delete()
            errors = "OTP Confirmation Fails!!. Please Try Again"
            context = {
                'errors': errors,
            }
            return render(request, 'src/userRegister.html', context)

    return render(request, 'src/userConfirmation.html')


def gatepassDelete(request, pk):
    gateLogout()
    if userid == -1:
        return render(request, 'src/loginError.html')
    else:
        visitor_obj = Visitor.objects.get(id=pk).delete()
        return HttpResponseRedirect('/userLogin/gatepass')


def userLogoutDone(request):
    logout()
    gateLogout()
    superLogout()
    return HttpResponseRedirect('/')


def gatepass(request):
    gateLogout()
    superLogout()
    # print(userid)
    if userid == -1:
        return render(request, 'src/loginError.html')
    else:
        gateid = Admin.objects.all()
        # print(gateid)
        user_admin_obj = User.objects.get(id=userid)
        context = {
            'gateid': gateid,
            'user_admin_obj': user_admin_obj,
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
    gateLogout()
    logout()
    superLogout()
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
            error = "Username you entered doesn't exist"
            return render(request, "src/adminLogin.html", {"error": error}, context)
        elif not user_admin_obj.password == password:
            errors = "Username and password didn't match"
            return render(request, "src/adminLogin.html", {"errors": errors}, context)
        superLogin(user_admin_obj.id)
        return HttpResponseRedirect('superAdminDash/')
        # return render(request,'src/superAdminDash.html')

    return render(request, "src/adminLogin.html", context)


def superAdminDash(request):
    gateLogout()
    logout()
    if superAdminId == -1:
        return render(request, 'src/loginError.html')
    else:
        admin_obj = Admin.objects.all()
        context = {
            'admin_obj': admin_obj,
        }
        if request.method == 'POST':
            gate = request.POST.get('gate')

            name = request.POST.get('name')
            password = request.POST.get('password')
            mail = request.POST.get('mail')
            contact = request.POST.get('contact')
            gender = request.POST.get('gender')

            adminData = Admin.objects.all()
            for i in range(len(adminData)):

                if(int(gate) == int(adminData[i].gate)):
                    print('g')
                    context = {
                        'admin_obj': admin_obj,
                        'error': "*This gateId is already exist",
                    }
                    return render(request, 'src/superAdminDash.html', context)

            admin = Admin(gate=gate, name=name,
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
                context = {
                    'admin_obj': admin_obj,
                    'errors': "*We fond the same email id in our data. It should be unique"
                }
                return render(request, 'src/superAdminDash.html', context)

        return render(request, 'src/superAdminDash.html', context)


def statistics(request):
    gateLogout()
    logout()
    if superAdminId == -1:
        return render(request, 'src/loginError.html')
    else:
        dayVisitor = [0]*10
        day = ['2000-03-12']*10
        c = 0

        l = []
        while(c < 10):
            day[c] = datetime.strftime(
                datetime.now() - timedelta(c), '%Y-%m-%d')
            visitor = Visitor.objects.all().filter(
                visitDate=day[c]).exclude(checkout=None)
            temp_user = TemporaryUser.objects.all().filter(
                visitDate=day[c]).exclude(checkout=None)
            # print(len(temp_user))
            dayVisitor[c] = len(visitor)+len(temp_user)
            c += 1
        x = 9
        while(x >= 0):
            dictio = {}
            dictio['y'] = dayVisitor[x]
            dictio['label'] = day[x]
            l.append(dictio)
            x -= 1
        # print(l)
        now = datetime.now().date()

        outerList = []
        currentYear = (now.year)

        x = str(currentYear)+"-01-01"
        sd = parse_date(x)
        c = 0
        while(1):
            innerList = []
            visitor = Visitor.objects.all().filter(visitDate=sd).exclude(checkout=None)
            temp_user = TemporaryUser.objects.all().filter(
                visitDate=sd).exclude(checkout=None)
            innerList.append(str(sd))
            innerList.append(len(visitor)+len(temp_user))
            outerList.append(innerList)
            td = datetime.strftime(sd + timedelta(1), '%Y-%m-%d')
            nd = parse_date(td)
            sd = nd

            if(nd > datetime.now().date()):
                break
        # print(outerList)

        graphData = json.dumps(l)
        yearData = json.dumps(outerList)
        length = json.dumps(len(outerList))
        context = {
            'graphData': graphData,
            'yearData': yearData,
            'len': length,
        }
        return render(request, 'src/statistics.html', context)


def adminEdit(request, pk):
    gateLogout()
    logout()
    if superAdminId == -1:
        return render(request, 'src/loginError.html')
    else:
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
                context = {
                    'admin_obj': admin_obj,
                    'errors': "*We fond the same email id in our data. It should be unique"
                }
                return render(request, 'src/adminEdit.html', context)

        return render(request, 'src/adminEdit.html', context)


def adminDelete(request, pk):
    gateLogout()
    logout()
    if superAdminId == -1:
        return render(request, 'src/loginError.html')
    else:
        admin_obj = Admin.objects.get(gate=pk).delete()

        return HttpResponseRedirect('/adminLogin/superAdminDash/')


def gateAdminLogin(request):
    gateLogout()
    logout()
    superLogout()
    gateid = Admin.objects.all()

    username = "GateId"
    type = "number"
    context = {
        'gateid': gateid,
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
            error = "Gate ID you entered doesn't exist"
            return render(request, "src/adminLogin.html", {"error": error}, context)
        elif not user_admin_obj.password == password:
            errors = "Gate Id and password didn't match"
            return render(request, "src/adminLogin.html", {"errors": errors}, context)

        gateLogin(gateId)

        #messages.info(request, 'Your password has been changed successfully!')
        return HttpResponseRedirect('gateAdminDash/')
        # return render(request,'src/superAdminDash.html')

    return render(request, "src/adminLogin.html", context)


def gateAdminDash(request):
    logout()
    superLogout()
    if gate_id == -1:
        return render(request, 'src/loginError.html')
    else:
        visitor_obj = Visitor.objects.all().filter(visitDate=datetime.now().date(),
                                                   checkout=None, gateId=gate_id).exclude(checkin=None)
        temp_user_obj = TemporaryUser.objects.all().filter(visitDate=datetime.now().date(),
                                                           checkout=None, gateId=gate_id).exclude(checkin=None)

        l = []
        for i in range(len(visitor_obj)):
            if visitor_obj[i].visiting_hour != "More Than 3":
                now = datetime.utcnow().replace(tzinfo=utc)
                diff = visitor_obj[i].checkin - now
                hour = 5.5-float(diff.total_seconds()/3600)
                if visitor_obj[i].visiting_hour == "1":
                    if hour > 1:
                        user_obj = (visitor_obj[i].userId)
                        l.append(user_obj.name)
                if visitor_obj[i].visiting_hour == "2":
                    if hour > 2:
                        user_obj = (visitor_obj[i].userId)
                        l.append(user_obj.name)
                if visitor_obj[i].visiting_hour == "3":
                    if hour > 3:
                        user_obj = (visitor_obj[i].userId)
                        l.append(user_obj.name)
        for i in range(len(temp_user_obj)):
            if temp_user_obj[i].visiting_hour != "More Than 3":
                now = datetime.utcnow().replace(tzinfo=utc)
                diff = temp_user_obj[i].checkin - now
                hour = 5.5-float(diff.total_seconds()/3600)
                if temp_user_obj[i].visiting_hour == "1":
                    if hour > 1:
                        #user_obj= (visitor_obj[i].userId)
                        l.append(temp_user_obj[i].name)
                if temp_user_obj[i].visiting_hour == "2":
                    if hour > 2:
                        #user_obj=  (visitor_obj[i].userId)
                        l.append(temp_user_obj[i].name)
                if temp_user_obj[i].visiting_hour == "3":
                    if hour > 3:
                        #user_obj=  (visitor_obj[i].userId)
                        l.append(temp_user_obj[i].name)
        # print(l)
        dueList = json.dumps(l)
        context = {
            'messages': dueList,
        }
        if request.method == 'POST':
            name = request.POST.get('name')
            mail = request.POST.get('mail')
            contact = request.POST.get('contact')
            gender = request.POST.get('gender')
            #photo = request.POST.get('photo')
            gateId = gate_id
            visit_gate = Admin.objects.get(gate=gateId)
            visitDate = datetime.now().date()
            visiting_hour = request.POST.get('visiting_hour')
            reason = request.POST.get('reason')
            checkin = datetime.now()
            user = TemporaryUser(name=name, mail=mail, contact=contact, gender=gender,  gateId=visit_gate,
                                 checkin=checkin, visitDate=visitDate, visiting_hour=visiting_hour, reason=reason)
            try:
                user.save()
                return render(request, 'src/gateAdminDash.html', context)
            except Exception as e:
                print(e)
                return render(request, 'src/gateAdminDash.html', context)

        return render(request, 'src/gateAdminDash.html', context)


def timeDue(request):
    logout()
    superLogout()
    if gate_id == -1:
        return render(request, 'src/loginError.html')
    else:
        obj = -1
        visitor_obj = Visitor.objects.all().filter(visitDate=datetime.now().date(),
                                                   checkout=None, gateId=gate_id).exclude(checkin=None)
        temp_user_obj = TemporaryUser.objects.all().filter(visitDate=datetime.now().date(),
                                                           checkout=None, gateId=gate_id).exclude(checkin=None)
        print(visitor_obj)
        l = []
        timeDue = []
        for i in range(len(visitor_obj)):

            if visitor_obj[i].visiting_hour != "More Than 3":

                now = datetime.utcnow().replace(tzinfo=utc)
                diff = visitor_obj[i].checkin - now
                print(visitor_obj[i].checkin)
                hour = 5.5-float(diff.total_seconds()/3600)
                if visitor_obj[i].visiting_hour == "1":
                    if hour > 1:
                        obj = 1
                        user_obj = (visitor_obj[i].userId)
                        l.append(user_obj.name)

                        timeDue.append(format(hour-1, '.2f'))
                if visitor_obj[i].visiting_hour == "2":
                    if hour > 2:
                        obj = 1
                        user_obj = (visitor_obj[i].userId)
                        l.append(user_obj.name)
                        timeDue.append(format(hour-2, '.2f'))
                if visitor_obj[i].visiting_hour == "3":
                    if hour > 3:
                        obj = 1
                        user_obj = (visitor_obj[i].userId)
                        l.append(user_obj.name)
                        timeDue.append(format(hour-3, '.2f'))

        for i in range(len(temp_user_obj)):
            if temp_user_obj[i].visiting_hour != "More Than 3":
                now = datetime.utcnow().replace(tzinfo=utc)
                diff = temp_user_obj[i].checkin - now
                # print(visitor_obj[i].checkin)
                hour = 5.5-float(diff.total_seconds()/3600)
                if temp_user_obj[i].visiting_hour == "1":
                    if hour > 1:
                        obj = 1
                        #user_obj= (visitor_obj[i].userId)
                        l.append(temp_user_obj[i].name)
                        timeDue.append(format(hour-1, '.2f'))
                if temp_user_obj[i].visiting_hour == "2":
                    if hour > 2:
                        obj = 1
                       # user_obj=  (visitor_obj[i].userId)
                        l.append(temp_user_obj[i].name)
                        timeDue.append(format(hour-2, '.2f'))
                if temp_user_obj[i].visiting_hour == "3":
                    if hour > 3:
                        obj = 1
                        #user_obj=  (visitor_obj[i].userId)
                        l.append(temp_user_obj[i].name)
                        timeDue.append(format(hour-3, '.2f'))

        # print(l)
        context = {
            'name': l,
            'time': timeDue,
            'obj': obj,
        }
        return render(request, 'src/timeDue.html', context)


def makeCheckIn(request):
    logout()
    superLogout()
    if gate_id == -1:
        return render(request, 'src/loginError.html')
    else:
        search = ' '
        if request.method == "POST":
            search = request.POST.get('search')

        try:
            visitor_obj = Visitor.objects.all().filter(
                checkin=None, gateId=gate_id, visitDate=datetime.now().date())
        except:
            visitor_obj = None
        obj = -1
        if visitor_obj is None or len(visitor_obj) == 0:
            context = {
                'obj': obj,
            }
            return render(request, 'src/makeCheckIn.html', context)
        else:
            l = []
            # print(search)
            user_obj = User.objects.all().filter(name__contains=search)
            for i in range(len(visitor_obj)):
                for j in range(len(user_obj)):

                    if visitor_obj[i].userId == user_obj[j]:
                        # x=visitor_obj[i].userId
                        # l[i]=x
                        l.append(visitor_obj[i].userId)
            obj = 1
            context = {
                'obj': obj,
                'visitor_obj': visitor_obj,
                'x': l,
                'len': len(visitor_obj),
            }
            return render(request, 'src/makeCheckIn.html', context)


def checkInVisitor(request, pk):
    logout()
    superLogout()
    if gate_id == -1:
        return render(request, 'src/loginError.html')
    else:
        print(pk)
        visitor_obj = Visitor.objects.get(
            id=pk, checkin=None, visitDate=datetime.now().date())
        visitor_obj.checkin = datetime.now()
        try:
            visitor_obj.save()

        except Exception as e:
            print(e)
        return HttpResponseRedirect('/makeCheckIn/')


def makeCheckOut(request):
    logout()
    superLogout()
    if gate_id == -1:
        return render(request, 'src/loginError.html')
    else:
        search = ' '
        if request.method == "POST":
            search = request.POST.get('search')

        obj = -1
        try:
            visitor_obj = Visitor.objects.all().filter(checkout=None, gateId=gate_id,
                                                       visitDate=datetime.now().date()).exclude(checkin=None)
        except:
            visitor_obj = None

        try:
            temp_user_obj = TemporaryUser.objects.all().filter(name__contains=search, checkout=None,
                                                               gateId=gate_id, visitDate=datetime.now().date()).exclude(checkin=None)
        except:
            temp_user_obj = None
        if (visitor_obj is None or len(visitor_obj) == 0) and (temp_user_obj is None or len(temp_user_obj) == 0):
            context = {
                'obj': obj,
            }
            return render(request, 'src/makeCheckOut.html', context)
        else:
            l = []
            user_obj = User.objects.all().filter(name__contains=search)
            for i in range(len(visitor_obj)):
                for j in range(len(user_obj)):

                    if visitor_obj[i].userId == user_obj[j]:
                        # x=visitor_obj[i].userId
                        # l[i]=x
                        l.append(visitor_obj[i].userId)
            obj = 1
            context = {
                'obj': obj,
                'visitor_obj': visitor_obj,
                'x': l,
                'len': len(visitor_obj),
                'temp_user_obj': temp_user_obj,
            }
            return render(request, 'src/makeCheckOut.html', context)


def checkOutVisitor(request, pk):
    logout()
    superLogout()
   # print(pk)
    if gate_id == -1:
        return render(request, 'src/loginError.html')
    else:
        visitor_obj = Visitor.objects.get(
            id=pk, checkout=None, visitDate=datetime.now().date())
        visitor_obj.checkout = datetime.now()
        try:
            visitor_obj.save()

        except Exception as e:
            print(e)
        return HttpResponseRedirect('/makeCheckOut/')


def checkOutTempVisitor(request, pk, type):
    logout()
    superLogout()
   # print(pk)
    if gate_id == -1:
        return render(request, 'src/loginError.html')
    else:
        tp_obj = TemporaryUser.objects.get(
            id=pk, checkout=None, visitDate=datetime.now().date())
        tp_obj.checkout = datetime.now()
        try:
            tp_obj.save()

        except Exception as e:
            print(e)
        return HttpResponseRedirect('/makeCheckOut/')


def checkOutDone(request):
    logout()
    superLogout()
    if gate_id == -1:
        return render(request, 'src/loginError.html')
    else:
        search = ' '
        if request.method == "POST":
            search = request.POST.get('search')

        obj = -1
        try:
            visitor_obj = Visitor.objects.all().filter(visitDate=datetime.now().date(),
                                                       gateId=gate_id).exclude(checkout=None)
            print(visitor_obj)
        except:
            visitor_obj = None
        try:
            temp_user_obj = TemporaryUser.objects.all().filter(name__contains=search,
                                                               gateId=gate_id, visitDate=datetime.now().date()).exclude(checkout=None)
        except:
            temp_user_obj = None
        if (visitor_obj is None or len(visitor_obj) == 0) and (temp_user_obj is None or len(temp_user_obj) == 0):
            context = {
                'obj': obj,
            }
            return render(request, 'src/checkOutDone.html', context)
        else:
            l = []
            user_obj = User.objects.all().filter(name__contains=search)
            for i in range(len(visitor_obj)):
                for j in range(len(user_obj)):

                    if visitor_obj[i].userId == user_obj[j]:
                        # x=visitor_obj[i].userId
                        # l[i]=x
                        l.append(visitor_obj[i].userId)
            obj = 1
            context = {
                'obj': obj,
                'visitor_obj': visitor_obj,
                'x': l,
                'len': len(visitor_obj),
                'temp_user_obj': temp_user_obj,
            }
            return render(request, 'src/checkOutDone.html', context)


def adminLogout(request):
    logout()
    gateLogout()
    superLogout()
    return HttpResponseRedirect('/')


def superAdminLogout(request):
    logout()
    gateLogout()
    superLogout()
    return HttpResponseRedirect('/')


def forgotPassword(request):
    if request.method == 'POST':
        mail = request.POST.get('mail')
        send_mail('Sending OTP for Pass Generation', "420 is the otp for your password",
                  "visitormanage10@gmail.com",
                  [mail],  # "list of recpetenets",
                  fail_silently=False
                  )
        return render(request, 'src/forgo')
    return render(request, 'src/forgotPassword.html')
