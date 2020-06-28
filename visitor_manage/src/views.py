from __future__ import unicode_literals

from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect
from .models import *
from django.db.models import Q
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
import django.contrib.messages
import datetime
from datetime import datetime, timedelta, timezone
import json
from django.core.files.storage import FileSystemStorage
import random
from django.conf import settings

userid = -1
gate_id = -1
superAdminId = -1
e_mail = ""
otp_f = 0
EMAIL_HOST_USER = settings.EMAIL_HOST_USER

# mail Id change


def supermail(mail, otp):
    global e_mail
    e_mail = mail
    global otp_f
    otp_f = otp

# change UserId when user login


def login(id):
    global userid
    userid = id

# Mange logout of User


def logout():
    global userid
    userid = -1

# Gate Admin Login


def gateLogin(id):
    global gate_id
    gate_id = id

# Gate Admin Logout


def gateLogout():
    global gate_id
    gate_id = -1

# Super Admin Login


def superLogin(id):
    global superAdminId
    superAdminId = id

# Super Admin Logout


def superLogout():
    global superAdminId
    superAdminId = -1

# Home Page


def index(request):
    logout()  # To manage Logout of each type of user
    gateLogout()
    superLogout()
    return render(request, 'src/frontPage.html')


"""
*On this page:
->User Login
    -Username Exist or not 
    - Username and Password Matches with any data of Database
    -If yes than login else Render the same page
->Can use Forget Password
    - User should write correct username and Email of his/her(as these are Unique)
    - Send Otp on Email
    - For verification purpose

*Return :
-> Previous visit:
    - Check If user already visited college, Then send him Feedback form(feedback Function)
-> No visit:
    -Check If user have already generated a Pass for his future visit
-> No pass :
    -Render to User Dash board such that one can create Gatpass

 """


def userLogin(request):
    logout()  # Logout of all type of users
    gateLogout()
    superLogout()
    if request.method == "POST":                                            # If Got response from Login Form
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(username)
        try:
            # Try fetch data from table with same username
            user_admin_obj = User.objects.get(username=username)
        except:
            # Username not Found!!
            user_admin_obj = None

        if user_admin_obj is None:
            error = "*Username you entered doesn't exist"
            messages.error(request, "Entered Username Doesn't Exist!!")
            # Username not found and render the same page
            return render(request, "src/userLogin.html", {"error": error})
        elif not user_admin_obj.password == password:
            errors = "*Invalid password"
            messages.error(request, "Wrong Password")
            # Given Username and password Field doesn't match with any data
            return render(request, "src/userLogin.html", {"errors": errors})
            # render the same page

        # Else user successfully loggedIn. Make Id as per one's Id
        login(user_admin_obj.id)
        try:
            visitor_obj = Visitor.objects.all().filter(userId=user_admin_obj.id,
                                                       feedback=None).exclude(Q(checkin=None) | Q(checkout=None))
            # Check Previous visit whose feedback field is null
            # So set feedback screen
        except:
            visitor_obj = None

        # No previous record found....
        if visitor_obj is None or len(visitor_obj) == 0:
            try:
                visitor_obj = Visitor.objects.all().filter(
                    Q(checkin=None) | Q(checkout=None), userId=user_admin_obj.id)
                # Try to fetch Already created Gatepass
            except:
                visitor_obj = None
            obj = -1

            # No gate pass found
            if visitor_obj is None or len(visitor_obj) == 0:
                context = {
                    'username': username,
                    'obj': obj,
                    'user_admin_obj': user_admin_obj,
                }
                # Simply render Dash Board
                messages.success(request, "Gate Pass Created!!")
                return render(request, 'src/userDash.html', context)
            else:                                                           # GatePass found
                obj = 1
                timeDue = ''
                try:
                    vs = Visitor.objects.get(~Q(checkin=None) & Q(checkout=None), userId=user_admin_obj)    
                except:
                    vs == None
                
                if vs is not None:
                    if vs.visiting_hour != "More Than 3":
                        now = datetime.utcnow().replace(tzinfo=utc)
                        if(now < vs.checkin):
                            diff = vs.checkin - now
                            hour = 5.5 - float(diff.total_seconds()/3600)
                        else:
                            diff = now-vs.checkin
                            hour = float(diff.total_seconds()/3600)

                        if vs.visiting_hour == "1":
                            if hour > 1:
                                timeDue = 'Your granted time expired. You are dued by ' + \
                                    format(hour-1, '.2f')+' hours.'
                        elif vs.visiting_hour == "2":
                            if hour > 2:
                                timeDue = 'Your granted time expired. You are dued by ' + \
                                    format(hour-2, '.2f')+' hours.'
                        else:
                            if hour > 3:
                                timeDue = 'Your granted time expired. You are dued by ' + \
                                    format(hour-3, '.2f')+' hours.'
                context = {
                'username': username,
                'obj': obj,
                'timeDue': timeDue,
                'visiter_obj': visitor_obj[0],
                'user_admin_obj': user_admin_obj,
                }

                messages.success(request, "Successfully Login into the system")
                # Show Gatepass on user Dashboard screen
                return render(request, 'src/userDash.html', context)
        else:
            messages.success(request, "Successfully Login into the system")
            return HttpResponseRedirect('/feedback/')  # Render Feedback form

    # No response of userLogin form
    return render(request, "src/userLogin.html")


"""
*On this page:
-Feedback form
*return:
-Gatepass screen
"""


def feedback(request):
    gateLogout()
    superLogout()
    if userid == -1:
        return render(request, 'src/loginError.html')
    else:
        user_admin_obj = User.objects.get(id=userid)
        context = {
            'user_admin_obj': user_admin_obj,
        }
        if request.method == "POST":
            feedback = request.POST.get('feedback')
            visitor_obj = Visitor.objects.get(
                (~Q(checkin=None) & ~Q(checkout=None)), userId=userid, feedback=None)
            print(visitor_obj)
            visitor_obj.feedback = feedback
            try:
                visitor_obj.save()
                return HttpResponseRedirect('/userLogin/gatepass')
            except Exception as e:
                print(e)
    return render(request, 'src/feedback.html', context)


"""
User enters His email and username
    - if match, send OTP
    -otherwise render on login

"""


def forgotPassword(request):
    if request.method == 'POST':
        mail = request.POST.get('mail')
        uname = request.POST.get('username')

        try:
            user = User.objects.get(username=uname)

            if mail == user.mail:
                otp = random.randint(1000, 9999)
                print(otp)
                send_mail('Forgot Password', "OTP for Changing your password is {}".format(otp),
                          EMAIL_HOST_USER,
                          [mail],  # "list of recpetenets",
                          fail_silently=False
                          )
                supermail(mail, otp)
                messages.info(
                    request, "OTP has been send to your Registered Email ID")
                return HttpResponseRedirect('/forgotPassword/otpForgot')
            else:
                context = {
                    'errors': "Email is Not registered"
                }
                messages.error(request, "Email is Not Registered")
                return render(request, 'src/emailSendForgot.html', context)
        except User.DoesNotExist:
            context = {
                'errors': "Username is Not registered"
            }
            messages.error(request, "Username is Not Registered")
            return render(request, 'src/emailSendForgot.html', context)
    return render(request, 'src/emailSendForgot.html')


"""
Allow user to enter otp , if match so allow him to reset password
                        else  shows an error
"""


def otpForgot(request):

    if request.method == 'POST':
        otp = request.POST.get('otpConfirm')
        print(otp_f)
        if otp_f == int(otp):
            return HttpResponseRedirect('/forgotPassword/setNewPassword')
        else:
            context = {
                'errors': "Wrong OTP Entered!!!"
            }
            messages.error(request, "OTP is not Correct")
            return render(request, 'src/otpForgot.html', context)

    return render(request, 'src/otpForgot.html')


def setNewPassword(request):

    if request.method == 'POST':
        passw = request.POST.get('password')
        cpassw = request.POST.get('cpassword')

        if passw == cpassw:
            user = User.objects.get(mail=e_mail)
            print(user.name)
            user.password = passw
            user.save()
            messages.success(request, "Your Password is updated")
            return HttpResponseRedirect('/userLogin/')
        else:
            context = {
                'errors': "Password Doesn't Match"
            }
            messages.error(request, "Password Doesn't Match")
            return render(request, 'src/setNewPassword.html', context)
    return render(request, 'src/setNewPassword.html')


"""
*On this Page:
->UserRegister:
    -Fetch the data from register form
->Both password:
    -Both not match ... render same page by showing the error
->Confirm Mail:
    -Send OTP to verify the email address. If entered OTP matches than only user
     will able to create an account

*Return:
->Both password Or data:
    - Wrong type of data enter, so render the same page with error
->Email :
    -If data entered varified then send OTP to verify email

"""


def userRegister(request):
    logout()  # logout all kind og users
    gateLogout()
    superLogout()
    # Got response from register form
    if request.method == 'POST':
        username = request.POST.get('username')
        name = request.POST.get('name')
        password = request.POST.get('password')
        cpassword = request.POST.get('cpassword')
        # Both passwords matches
        if cpassword == password:
            mail = request.POST.get('mail')
            # Create an OTP and send on given email
            otp = random.randint(1000, 9999)
            send_mail("Confirmation Mail", "OTP for the User Confirmation is {}".format(otp),
                      EMAIL_HOST_USER,
                      [mail],
                      fail_silently=False
                      )

            supermail(mail, otp)
            contact = request.POST.get('contact')
            gender = request.POST.get('gender')
            photo = request.FILES['photo']
            fs = FileSystemStorage()
            fs.save(photo.name, photo)

            user = User(username=username, name=name, password=password,                        # Create object of table to store the data
                        mail=mail, contact=contact, gender=gender, photo=photo)
            try:  # If form successfully verified.. Then goto OTP
                # Function to verify email
                obj = -1
                user.save()
                login(user.id)

                return HttpResponseRedirect('/userRegister/userConfirmation')
                # return render(request, 'src/userDash.html', context)
            # Form not verified. So some error show on same page
            except Exception as e:
                print(e)
                errors = "*We found the same username or email id in our data. These should be unique. Try some new"
                context = {
                    'errors': errors,
                }
                messages.error(
                    request, "Username or Email id is already Registered!")
                return render(request, 'src/userRegister.html', context)
        # Both passwords doesn't match
        else:
            context = {
                'errors': "Password Doesn't Matches!!. Please Try Again.",
            }
            messages.error(request, "Password Doesn't Matches")
            return render(request, 'src/userRegister.html', context)
    return render(request, 'src/userRegister.html')


"""
*On this page:
->Enter OTP which was sent on your mail.. to verify the mailId
*Return:
->OTP match:
    -render User DashBoard
    -Succesfully account created
->Not match:
    -Account is not created
    -Goto register page
"""


def userConfirmation(request):
    gateLogout()
    superLogout()
    if userid == -1:
        return render(request, 'src/loginError.html')
    else:
        if request.method == "POST":  # fetch data from OTP form
            OTP = int(request.POST.get('otpConfirm'))

            if OTP == otp_f:  # OTP match, goto user dashboard
                user_admin_obj = User.objects.get(id=userid)
                username = user_admin_obj.username
                context = {
                    'username': username,
                    'user_admin_obj': user_admin_obj,
                }

                return render(request, 'src/userDash.html', context)
            else:  # Delete user object with same Id
                User.objects.get(id=userid).delete()
                errors = "OTP Confirmation Fails!!. Please Try Again"
                context = {
                    'errors': errors,
                }
                messages.error(
                    request, "OTP Confirmation Fails!!. Please Try Again")
                return render(request, 'src/userRegister.html', context)

        return render(request, 'src/userConfirmation.html')


"""
 Allow user to make gatepass
"""


def gatepass(request):
    gateLogout()
    superLogout()

    if userid == -1:
        return render(request, 'src/loginError.html')
    else:

        user_admin_obj = User.objects.get(id=userid)
        context = {
            'user_admin_obj': user_admin_obj,
        }
        if request.method == 'POST':

            userId = userid
            visitDate = request.POST.get('visitDate')
            visiting_hour = request.POST.get('visiting_hour')
            reason = request.POST.get('reason')
            #visit_gate = Admin.objects.get(gate=gateId)
            user_id = User.objects.get(id=userId)

            visitor = Visitor(userId=user_id,
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

                send_mail("Your Visitor Pass", "Your Visitor Pass has been Successfully Created\n"
                          + " You can Show this Mail to Enter in the College\n\n"
                          + "Name : {}\n".format(user_id.username)
                          + "Gender : {}\n".format(user_admin_obj.gender)
                          + "Date of Visit: {}\n".format(visitor.visitDate)
                          + "Reason of Visit: {}\n".format(visitor.reason)
                          + "Time validity: {} Hour\n".format(visitor.visiting_hour),
                          EMAIL_HOST_USER,
                          [user_admin_obj.mail],
                          fail_silently=False
                          )

                return render(request, 'src/userDash.html', context)
            except Exception as e:
                print(e)
                return render(request, 'src/gatepass.html', context)

        return render(request, 'src/gatepass.html', context)


# Allow user to delete gatepass.. If it is expriered

def gatepassDelete(request, pk):
    gateLogout()
    if userid == -1:
        return render(request, 'src/loginError.html')
    else:
        visitor_obj = Visitor.objects.get(id=pk).delete()
        return HttpResponseRedirect('/userLogin/gatepass')

def faq(request):
    gateLogout()
    superLogout()

    if userid == -1:
        return render(request, 'src/loginError.html')
    else:
        faq_obj = Faq.objects.all().exclude(answer=None)
        user=[]
        for i in range(len(faq_obj)):
            user.append(faq_obj[i].userId)
        obj=1
        context={
            'faq': faq_obj,
            'user':user,
            'basefile':"src/userNav.html",
            'obj':obj,
        }
        if request.method == 'POST':
            question= request.POST.get('question')
            user_obj=User.objects.get(id=userid)
            faq= Faq(question=question, userId= user_obj)
            try:
                faq.save()
            except Exception as e:
                print(e)
    return render(request, 'src/faq.html',context)

def faqCommon(request):
    gateLogout()
    logout()
    superLogout()
    faq_obj = Faq.objects.all().exclude(answer=None)
    user=[]
    for i in range(len(faq_obj)):
        user.append(faq_obj[i].userId)
    context={
            'faq': faq_obj,
            'user':user,
            'basefile':"src/base.html",
        }
    return render(request, 'src/faq.html',context)  

def faqAdmin(request):
    gateLogout()
    logout()
    if superAdminId==-1:
        return render(request, 'src/loginError.html')
    else:
        if request.method == 'POST':
            ans= request.POST.get('answer')
            que=request.POST.get('que')
            faq= Faq.objects.get(id=int(que))
            faq.answer=ans
            faq.save()
        faq_obj = Faq.objects.all().filter(answer=None)
        user=[]
        for i in range(len(faq_obj)):
            user.append(faq_obj[i].userId)
        context={
            'faq': faq_obj,
            'user':user,
        }

    return render(request, 'src/faqAdmin.html',context)       


def faqDelete(request,pk):
    gateLogout()
    logout()
    if superAdminId==-1:
        return render(request, 'src/loginError.html')
    else:
        faq_obj = Faq.objects.get(id=pk).delete()
    return HttpResponseRedirect('/faqAdmin/')


# User logout
def userLogoutDone(request):
    logout()
    gateLogout()
    superLogout()
    return HttpResponseRedirect('/')


"""
These function is login function for Super Admin 

"""


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
            messages.error(request, "Username doesn't exist")
            return render(request, "src/adminLogin.html", context)
        elif not user_admin_obj.password == password:
            errors = "Username and password didn't match"
            messages.error(request, "Username and Password didn't match")
            return render(request, "src/adminLogin.html", context)
        superLogin(user_admin_obj.id)
        messages.success(request, "Successfully Log in into the System")
        return HttpResponseRedirect('superAdminDash/')
        # return render(request,'src/superAdminDash.html')

    return render(request, "src/adminLogin.html", context)


"""
*Super Admin's dashboard
    -can add admin
    -can view, edit, delete admins
"""


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
                messages.error(request, "Email id is already Registered")
                return render(request, 'src/superAdminDash.html', context)

        return render(request, 'src/superAdminDash.html', context)

# fetch number of visitors of last 10 days and from the starting of the year to till now


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
                visitDate=day[c]).exclude(Q(checkin=None) | Q(checkout=None))
            print(visitor)
            temp_user = TemporaryUser.objects.all().filter(
                visitDate=day[c]).exclude(checkout=None)

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
            visitor = Visitor.objects.all().filter(
                visitDate=sd).exclude(Q(checkin=None) | Q(checkout=None))
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

# Super admin can view daily list of visitors


def viewVisitor(request):
    logout()
    gateLogout()
    if superAdminId == -1:
        return render(request, 'src/loginError.html')
    else:
        search = ''
        if request.method == "POST":
            search = request.POST.get('search')
        obj = -1
        try:
            visitor_obj = Visitor.objects.all().filter(
                visitDate=datetime.now().date()).exclude(checkout=None)

        except:
            visitor_obj = None
        try:
            temp_user_obj = TemporaryUser.objects.all().filter(
                name__contains=search, visitDate=datetime.now().date()).exclude(checkout=None)
        except:
            temp_user_obj = None
        if (visitor_obj is None or len(visitor_obj) == 0) and (temp_user_obj is None or len(temp_user_obj) == 0):
            context = {
                'obj': obj,
            }
            return render(request, 'src/viewVisitor.html', context)
        else:
            l = []
            user_obj = User.objects.all().filter(name__contains=search)
            for i in range(len(visitor_obj)):
                for j in range(len(user_obj)):

                    if visitor_obj[i].userId == user_obj[j]:
                        l.append(visitor_obj[i].userId)
            obj = 1
            context = {
                'obj': obj,
                'visitor_obj': visitor_obj,
                'x': l,
                'len': len(visitor_obj),
                'temp_user_obj': temp_user_obj,
            }
            return render(request, 'src/viewVisitor.html', context)

# super admin can add,view, delete image from gallery


def imageGallery(request):
    gateLogout()
    logout()
    if superAdminId == -1:
        return render(request, 'src/loginError.html')
    else:
        obj = 1
        img1 = ImageGallery.objects.all()
        img2 = ImageUpload.objects.all()
        user = []
        for i in range(len(img2)):
            user.append(img2[i].userId)
        context = {
            'obj': obj,
            'img1': img1,
            'img2': img2,
            'user': user,
            'basefile': "src/superAdminBasefile.html",
        }
        if request.method == 'POST':
            photo = request.FILES['photo']
            fs = FileSystemStorage()
            fs.save(photo.name, photo)
            image = ImageGallery(photo=photo)
            try:
                image.save()
                img1 = ImageGallery.objects.all()
                context = {
                    'obj': obj,
                    'img1': img1,
                    'img2': img2,
                    'user': user2,
                    'basefile': "src/superAdminBasefile.html",
                }
            except Exception as e:
                print(e)

        return render(request, 'src/imageGallery.html', context)

# On Home screen everyone can view it


def imageGalleryUser(request):
    img1 = ImageGallery.objects.all()
    img2 = ImageUpload.objects.all()

    context = {
        'img1': img1,
        'img2': img2,
        'basefile': "src/base.html",
    }
    return render(request, 'src/imageGallery.html', context)

# delte image


def imageDelete(request, pk):
    gateLogout()
    logout()
    if superAdminId == -1:
        return render(request, 'src/loginError.html')
    else:
        im = ImageGallery.objects.get(id=pk).delete()

        return HttpResponseRedirect('/imageGallery/')


def imageDeleteUser(request, pk, us):
    gateLogout()
    logout()
    if superAdminId == -1:
        return render(request, 'src/loginError.html')
    else:
        im = ImageUpload.objects.get(id=pk).delete()

        return HttpResponseRedirect('/imageGallery/')

# Registered user can only upload the images


def imageUpload(request):
    gateLogout()
    superLogout()
    if userid == -1:
        return render(request, 'src/loginError.html')
    else:
        user_admin_obj = User.objects.get(id=userid)
        objt = 1
        img1 = ImageGallery.objects.all()
        img2 = ImageUpload.objects.all()
        user = []
        for i in range(len(img2)):
            user.append(img2[i].userId)
        context = {
            'objt': objt,
            'img1': img1,
            'img2': img2,
            'user': user,
            'basefile': "src/userNav.html",
            'user_admin_obj': user_admin_obj,
            'username': user_admin_obj.username

        }
        if request.method == 'POST':
            photo = request.FILES['photo']
            fs = FileSystemStorage()
            fs.save(photo.name, photo)
            userObj = User.objects.get(id=userid)
            image = ImageUpload(photo=photo, userId=userObj)
            try:
                image.save()
                img2 = ImageUpload.objects.all()
                user = []
                for i in range(len(img2)):
                    user.append(img2[i].userId)
                context = {
                    'objt': objt,
                    'img1': img1,
                    'img2': img2,
                    'user': user,
                    'basefile': "src/userNav.html",
                    'user_admin_obj': user_admin_obj,
                }

            except Exception as e:
                print(e)

        return render(request, 'src/imageGallery.html', context)

# Super admin can view and delete review


def review(request):
    gateLogout()
    logout()
    if superAdminId == -1:
        return render(request, 'src/loginError.html')
    else:
        visitor_obj = Visitor.objects.all().exclude(feedback=None)
        user = []
        for i in range(len(visitor_obj)):
            user.append(visitor_obj[i].userId)
        obj = 1
        context = {
            'visitor_obj': visitor_obj,
            'user': user,
            'obj': obj,
            'basefile': "src/superAdminBasefile.html",

        }
        return render(request, 'src/review.html', context)

# On home screen every one can view feedback and who wrote it


def reviewHome(request):
    gateLogout()
    logout()
    superLogout()
    visitor_obj = Visitor.objects.all().exclude(feedback=None)
    user = []
    for i in range(len(visitor_obj)):
        user.append(visitor_obj[i].userId)
    context = {
        'visitor_obj': visitor_obj,
        'basefile': "src/base.html",
        'user': user,
    }
    return render(request, 'src/review.html', context)

# Super admin can delete review means make it None


def deleteReview(request, pk):
    gateLogout()
    logout()
    if superAdminId == -1:
        return render(request, 'src/loginError.html')
    else:
        visitor = Visitor.objects.get(id=pk)
        visitor.feedback = None
        try:
            visitor.save()
        except Exception as e:
            print(e)
    return HttpResponseRedirect('/review')


# home screen map, location of AU and SEAS , but you have to use your API to see the map


def location(request):
    return render(request, 'src/location.html')

# Super admin can edit gate admin's details


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
                messages.error(request, "Email id is already Registered")
                return render(request, 'src/adminEdit.html', context)

        return render(request, 'src/adminEdit.html', context)

# Delete gatadmin


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
        if user_admin_obj is None:
            messages.error(request, "Entered Gate ID doesn't Exist")
            return render(request, "src/adminLogin.html", context)
        elif not user_admin_obj.password == password:
            messages.error(request, "Wrong Password")
            return render(request, "src/adminLogin.html", context)

        gateLogin(gateId)

        return HttpResponseRedirect('gateAdminDash/')

    return render(request, "src/adminLogin.html", context)


"""
-Here gate admin can make on the spot pass of visitor
-Before that if any user's time duration exceeds his/her aproved duration, 
 it shows list of names of those guys 
"""


def gateAdminDash(request):
    logout()
    superLogout()
    if gate_id == -1:
        return render(request, 'src/loginError.html')
    else:
        visitor_obj = Visitor.objects.all().filter(visitDate=datetime.now().date(),
                                                   checkout=None, gateId1=gate_id).exclude(checkin=None)
        temp_user_obj = TemporaryUser.objects.all().filter(visitDate=datetime.now().date(),
                                                           checkout=None, gateId1=gate_id).exclude(checkin=None)

        print(len(visitor_obj))
        l = []
        for i in range(len(visitor_obj)):
            if visitor_obj[i].visiting_hour != "More Than 3":
                now = datetime.utcnow().replace(tzinfo=utc)
                if(now < visitor_obj[i].checkin):
                    diff = visitor_obj[i].checkin - now
                    hour = 5.5 - float(diff.total_seconds()/3600)
                else:
                    diff = now-visitor_obj[i].checkin
                    hour = float(diff.total_seconds()/3600)

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
                if(now < temp_user_obj[i].checkin):
                    diff = temp_user_obj[i].checkin - now
                    hour = 5.5 - float(diff.total_seconds()/3600)
                else:
                    diff = now-temp_user_obj[i].checkin
                    hour = float(diff.total_seconds()/3600)

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
            gateId1 = gate_id
            #visit_gate = Admin.objects.get(gate=gateId1)
            visitDate = datetime.now().date()
            visiting_hour = request.POST.get('visiting_hour')
            reason = request.POST.get('reason')
            checkin = datetime.now()
            user = TemporaryUser(name=name, mail=mail, contact=contact, gender=gender,  gateId1=gateId1,
                                 checkin=checkin, visitDate=visitDate, visiting_hour=visiting_hour, reason=reason)

            try:
                user.save()
                send_mail("Your Visitor Pass", "Your Visitor Pass has been Successfully Created\n"
                          + " You can Show this Mail to Enter in the College\n\n"
                          + "Name : {}\n".format(user.name)
                          + "Gender : {}\n".format(user.gender)
                          + "Date of Visit: {}\n".format(user.visitDate)
                          + "Reason of Visit: {}\n".format(user.reason)
                          + "Time validity: {} Hour\n".format(user.visiting_hour)
                          + "Entry Gate Number: {}\n".format(user.gateId1),
                          EMAIL_HOST_USER,
                            [user.mail],
                            fail_silently=False
                          )
                return render(request, 'src/gateAdminDash.html', context)
            except Exception as e:
                print(e)
                return render(request, 'src/gateAdminDash.html', context)

        return render(request, 'src/gateAdminDash.html', context)

# show list of names and overdue time


def timeDue(request):
    logout()
    superLogout()
    if gate_id == -1:
        return render(request, 'src/loginError.html')
    else:
        obj = -1
        visitor_obj = Visitor.objects.all().filter(visitDate=datetime.now().date(),
                                                   checkout=None, gateId1=gate_id).exclude(checkin=None)
        temp_user_obj = TemporaryUser.objects.all().filter(visitDate=datetime.now().date(),
                                                           checkout=None, gateId1=gate_id).exclude(checkin=None)
        print(len(visitor_obj))
        l = []
        timeDue = []
        contact = []
        for i in range(len(visitor_obj)):
            print(visitor_obj[i].checkin)
            if visitor_obj[i].visiting_hour != "More Than 3":
                namePhone = []
                now = datetime.utcnow().replace(tzinfo=utc)
                if(now < visitor_obj[i].checkin):
                    diff = visitor_obj[i].checkin - now
                    hour = 5.5 - float(diff.total_seconds()/3600)
                else:
                    diff = now-visitor_obj[i].checkin
                    hour = float(diff.total_seconds()/3600)

                if visitor_obj[i].visiting_hour == "1":
                    if hour > 1:
                        obj = 1
                        user_obj = (visitor_obj[i].userId)
                        namePhone.append(user_obj.name)
                        namePhone.append(user_obj.contact)
                        timeDue.append(format(hour-1, '.2f'))
                        l.append(namePhone)
                if visitor_obj[i].visiting_hour == "2":
                    if hour > 2:
                        obj = 1
                        user_obj = (visitor_obj[i].userId)
                        namePhone.append(user_obj.name)
                        namePhone.append(user_obj.contact)
                        timeDue.append(format(hour-2, '.2f'))
                        l.append(namePhone)
                if visitor_obj[i].visiting_hour == "3":
                    if hour > 3:
                        obj = 1
                        user_obj = (visitor_obj[i].userId)
                        namePhone.append(user_obj.name)
                        namePhone.append(user_obj.contact)
                        timeDue.append(format(hour-3, '.2f'))
                        l.append(namePhone)

        for i in range(len(temp_user_obj)):
            if temp_user_obj[i].visiting_hour != "More Than 3":
                namePhone = []
                now = datetime.utcnow().replace(tzinfo=utc)
                if(now < temp_user_obj[i].checkin):
                    diff = temp_user_obj[i].checkin - now
                    hour = 5.5 - float(diff.total_seconds()/3600)
                else:
                    diff = now-temp_user_obj[i].checkin
                    hour = float(diff.total_seconds()/3600)

                if temp_user_obj[i].visiting_hour == "1":
                    if hour > 1:
                        obj = 1
                        namePhone.append(temp_user_obj[i].name)
                        namePhone.append(temp_user_obj[i].contact)
                        l.append(namePhone)
                        timeDue.append(format(hour-1, '.2f'))
                if temp_user_obj[i].visiting_hour == "2":
                    if hour > 2:
                        obj = 1
                        namePhone.append(temp_user_obj[i].name)
                        namePhone.append(temp_user_obj[i].contact)
                        l.append(namePhone)
                        timeDue.append(format(hour-2, '.2f'))
                if temp_user_obj[i].visiting_hour == "3":
                    if hour > 3:
                        obj = 1
                        namePhone.append(temp_user_obj[i].name)
                        namePhone.append(temp_user_obj[i].contact)
                        l.append(namePhone)
                        timeDue.append(format(hour-3, '.2f'))

        # print(l)
        context = {
            'namephone': l,
            'time': timeDue,
            'obj': obj,

        }
        return render(request, 'src/timeDue.html', context)

# shows the list of checkIn pending guys


def makeCheckIn(request):
    logout()
    superLogout()
    if gate_id == -1:
        return render(request, 'src/loginError.html')
    else:
        search = ''
        if request.method == "POST":
            search = request.POST.get('search')

        try:
            visitor_obj = Visitor.objects.all().filter(
                checkin=None, visitDate=datetime.now().date())
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
            user_obj = User.objects.all().filter(name__contains=search)
            for i in range(len(visitor_obj)):
                for j in range(len(user_obj)):
                    if visitor_obj[i].userId == user_obj[j]:
                        l.append(visitor_obj[i].userId)
            obj = 1
            context = {
                'obj': obj,
                'visitor_obj': visitor_obj,
                'x': l,
                'len': len(visitor_obj),
            }
            return render(request, 'src/makeCheckIn.html', context)

# mark as checkin


def checkInVisitor(request, pk):
    logout()
    superLogout()
    if gate_id == -1:
        return render(request, 'src/loginError.html')
    else:
        print(pk)
        visitor_obj = Visitor.objects.get(
            id=pk, checkin=None, visitDate=datetime.now().date())
        print(visitor_obj)
        visitor_obj.checkin = datetime.now()
        #visit_gate = Admin.objects.get(gate=gate_id)
        visitor_obj.gateId1 = gate_id
        try:
            visitor_obj.save()

        except Exception as e:
            print(e)
        return HttpResponseRedirect('/makeCheckIn/')

# shows the list of checkOut pending guys, who are in the college


def makeCheckOut(request):
    logout()
    superLogout()
    if gate_id == -1:
        return render(request, 'src/loginError.html')
    else:
        search = ''
        if request.method == "POST":
            search = request.POST.get('search')

        obj = -1
        try:
            visitor_obj = Visitor.objects.all().filter(checkout=None,
                                                       visitDate=datetime.now().date()).exclude(checkin=None)
        except:
            visitor_obj = None

        try:
            temp_user_obj = TemporaryUser.objects.all().filter(name__contains=search, checkout=None,
                                                               visitDate=datetime.now().date()).exclude(checkin=None)
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

# mark as checkout


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
        visitor_obj.gateId2 = gate_id
        try:
            visitor_obj.save()

        except Exception as e:
            print(e)
        return HttpResponseRedirect('/makeCheckOut/')

# to checkout temporary on the spot visitors


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
        tp_obj.gateId2 = gate_id
        try:
            tp_obj.save()

        except Exception as e:
            print(e)
        return HttpResponseRedirect('/makeCheckOut/')

# shows the list of visit done guys


def checkOutDone(request):
    logout()
    superLogout()
    if gate_id == -1:
        return render(request, 'src/loginError.html')
    else:
        search = ''
        if request.method == "POST":
            search = request.POST.get('search')

        obj = -1
        try:
            visitor_obj = Visitor.objects.all().filter(visitDate=datetime.now().date(),
                                                       gateId2=gate_id).exclude(checkout=None)

        except:
            visitor_obj = None
        try:
            temp_user_obj = TemporaryUser.objects.all().filter(name__contains=search,
                                                               gateId2=gate_id, visitDate=datetime.now().date()).exclude(checkout=None)
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
