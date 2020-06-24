from django.urls import path
from . import views
from .views import *
urlpatterns = [
    path('', views.index, name='index'),
    path('userLogin/', views.userLogin, name='userLogin'),
    path('userRegister/', views.userRegister, name='userRegister'),
    path('userLogin/gatepass', views.gatepass, name='gatepass'),
    path('userRegister/userConfirmation',
         views.userConfirmation, name='userConfirmation'),

    path('forgotPassword/', views.forgotPassword, name='forgotPassword'),
    path('forgotPassword/otpForgot', views.otpForgot, name='otpForgot'),
    path('forgotPassword/setNewPassword',
         views.setNewPassword, name='setNewPassword'),

    path('userRegister/gatepass', views.gatepass, name='gatepass'),
    path('gatepassDelete/<int:pk>', views.gatepassDelete, name='gatepassDelete'),
    path('userLogoutDone/', views.userLogoutDone, name='userLogoutDone'),

    path('adminLogin/', views.adminLogin, name='adminLogin'),
    path('adminEdit/<int:pk>', views.adminEdit, name='adminEdit'),
    path('adminDelete/<int:pk>', views.adminDelete, name='adminDelete'),
    path('adminLogin/superAdminDash/',
         views.superAdminDash, name='superAdminDash'),
    path('statistics/', views.statistics, name='statistics'),
    path('superAdminLogout/', views.superAdminLogout, name='superAdminLogout'),


    path('gateAdminLogin/', views.gateAdminLogin, name='gateAdminLogin'),
    path('gateAdminLogin/gateAdminDash/',
         views.gateAdminDash, name='gateAdminDash'),
    path('makeCheckIn/', views.makeCheckIn, name='makeCheckIn'),
    path('makeCheckIn/<int:pk>', views.checkInVisitor, name='checkInVisitor'),
    path('makeCheckOut/', views.makeCheckOut, name='makeCheckOut'),
    path('makeCheckOut/<int:pk>', views.checkOutVisitor, name='checkOutVisitor'),
    path('makeCheckOut/<int:pk>/<str:type>',
         views.checkOutTempVisitor, name='checkOutTempVisitor'),
    path('checkOutDone', views.checkOutDone, name='checkOutDone'),
    path('timeDue/', views.timeDue, name='timeDue'),
    path('adminLogout/', views.adminLogout, name='adminLogout'),

]
