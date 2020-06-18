from django.urls import path
from . import views
from .views import *
urlpatterns = [
    path('', views.index, name='index'),
    path('userLogin/', views.userLogin, name='userLogin'),
    path('userRegister/', views.userRegister, name='userRegister'),
    path('userLogin/gatepass', views.gatepass, name='gatepass'),
    path('userRegister/gatepass', views.gatepass, name='gatepass'),

]