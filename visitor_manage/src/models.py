from django.db import models

# Create your models here.
GENDER = [
    ('male', 'Male'),
    ('female', 'Female'),
    ('other', 'Other'),
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
    gender = models.CharField(max_length=10)

    def __str__(self):
        return str(self.gate)


class User(models.Model):
    username = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=100)
    password = models.CharField(max_length=20)
    mail = models.EmailField(unique=True)
    contact = models.IntegerField()
    gender = models.CharField(max_length=10)
    photo = models.ImageField(upload_to='gallery')
    #bdate = models.DateField(auto_now_add=True)

    def __str__(self):
        return str(self.id)


class Visitor(models.Model):
    gateId = models.ForeignKey(Admin, default=1, on_delete=models.SET_DEFAULT)
    userId = models.ForeignKey(User, default=1, on_delete=models.SET_DEFAULT)
    visitDate = models.DateField()
    checkin = models.DateTimeField(null=True)
    checkout = models.DateTimeField(null=True)
    feedback = models.TextField(null=True)
    visiting_hour = models.CharField(max_length=20, default=1)
    reason = models.TextField(max_length=1000)

    def __str__(self):
        return str(self.id)
