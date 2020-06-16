from django.db import models

# Create your models here.
GENDER= [
    ('male', 'Male'),
    ('female', 'Female'),
    ('other', 'Other'),
    ]
class user(models.Model):
    username=models.CharField(max_length=50, unique=True)
    name=models.CharField(max_length=100)
    password=models.CharField(max_length=12)
    mail=models.CharField(max_length=100)
    contact=models.IntegerField()
    gender=models.CharField(max_length=10 ,choices=GENDER)
    photo=models.ImageField()