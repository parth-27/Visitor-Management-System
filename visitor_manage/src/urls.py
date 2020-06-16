from django.urls import path
from . import views
from .views import *
urlpatterns = [
    path('', views.index, name='index'),
    path('user/',views.userLogin,name='userLogin'),
    path('userRegister/',views.userRegister,name='userRegister'),
]