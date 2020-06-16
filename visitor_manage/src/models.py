from django.db import models

# Create your models here.
GENDER = [
    ('male', 'Male'),
    ('female', 'Female'),
    ('other', 'Other'),
]

VISITING_HOURS = [
    (1),
    (2),
    (3),
    ("More than 3"),
]


class SuperAdmin(models.Model):
    username = models.CharField(max_length=200)
    password = models.CharField(max_length=20)

    def __str__(self):
        return self.username


class Admin(models.Model):
    gate = models.IntegerField(primary_key=True)
    username = models.CharField(max_length=200, unique=True)
    name = models.CharField(max_length=100)
    password = models.CharField(max_length=20)
    mail = models.EmailField(unique=True)
    contact = models.IntegerField()
    gender = models.CharField(max_length=10, choices=GENDER)


class User(models.Model):
    username = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=100)
    password = models.CharField(max_length=20)
    mail = models.EmailField(unique=True)
    contact = models.IntegerField()
    gender = models.CharField(max_length=10, choices=GENDER)
    photo = models.ImageField()
    bdate = models.DateField()

    def __str__(self):
        return self.username


class Visitor(models.Model):
    gateId = models.ForeignKey(Admin, default=1, on_delete=models.SET_DEFAULT)
    userId = models.ForeignKey(User, default=1, on_delete=models.SET_DEFAULT)
    visitDate = models.DateField()
    checkin = models.DateTimeField()
    checkout = models.DateTimeField()
    feedback = models.TextField()
    reason = models.TextField(max_length=1000)
