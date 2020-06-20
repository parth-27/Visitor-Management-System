from django.urls import path
from . import views
from .views import *
urlpatterns = [
    path('', views.index, name='index'),
    path('userLogin/', views.userLogin, name='userLogin'),
    path('userRegister/', views.userRegister, name='userRegister'),
    path('userLogin/gatepass', views.gatepass, name='gatepass'),
    path('userRegister/gatepass', views.gatepass, name='gatepass'),

    path('adminLogin/', views.adminLogin, name='adminLogin'),
    path('adminEdit/<int:pk>', views.adminEdit, name='adminEdit'),
    path('adminDelete/<int:pk>', views.adminDelete, name='adminDelete'),
    path('adminLogin/superAdminDash/',
         views.superAdminDash, name='superAdminDash'),


    path('gateAdminLogin/', views.gateAdminLogin, name='gateAdminLogin'),
    path('gateAdminLogin/gateAdminDash/',
         views.gateAdminDash, name='gateAdminDash'),
    path('makeCheckIn/', views.makeCheckIn, name='makeCheckIn'),
    path('makeCheckIn/<int:pk>', views.checkInVisitor, name='checkInVisitor'),
    path('makeCheckOut/', views.makeCheckOut, name='makeCheckOut'),
    path('makeCheckOut/<int:pk>', views.checkOutVisitor, name='checkOutVisitor'),
    path('checkOutDone', views.checkOutDone, name='checkOutDone'),
    # path('forgotPassword/', views.sendMail),

]
