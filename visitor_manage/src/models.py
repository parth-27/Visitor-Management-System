from django.db import models

# Create your models here.


class SuperAdmin(models.Model):
    username = models.CharField(max_length=200)
    password = models.CharField(max_length=20)

    def __str__(self):
        return self.username


class Admin(models.Model):
    gate = models.IntegerField(primary_key=True)
    #username = models.CharField(max_length=200, unique=True)
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
    photo = models.ImageField()
    #bdate = models.DateField(auto_now_add=True)

    def __str__(self):
        return str(self.id)



class Visitor(models.Model):
    gateId1 = models.IntegerField(null=True)
    gateId2 = models.IntegerField(null=True)
    userId = models.ForeignKey(User, default=1, on_delete=models.SET_DEFAULT)
    visitDate = models.DateField()
    checkin = models.DateTimeField(null=True)
    checkout = models.DateTimeField(null=True)
    feedback = models.TextField(null=True)
    visiting_hour = models.CharField(max_length=20, default=1)
    reason = models.TextField(max_length=1000)
    mailDue = models.IntegerField(default=0)

    def __str__(self):
        return str(self.id)


class TemporaryUser(models.Model):
    name = models.CharField(max_length=100)
    mail = models.EmailField(max_length=320)
    contact = models.IntegerField()
    gender = models.CharField(max_length=10)
    photo = models.ImageField(upload_to='gallery', default='/tempUser.png')
    gateId1 = models.IntegerField(null=True)
    gateId2 = models.IntegerField(null=True)
    visitDate = models.DateField()
    checkin = models.DateTimeField(null=True)
    checkout = models.DateTimeField(null=True)
    feedback = models.TextField(null=True)
    visiting_hour = models.CharField(max_length=20, default=1)
    reason = models.TextField(max_length=1000)
    mailDue = models.IntegerField(default=0)
    def __str__(self):
        return str(self.id)

class ImageGallery(models.Model):
    photo = models.ImageField(upload_to='gallery', default='/tempUser.png')
    def __str__(self):
        return str(self.id)

class ImageUpload( models.Model):
    photo = models.ImageField(upload_to='gallery', default='/tempUser.png')
    userId = models.ForeignKey(User, default=1, on_delete=models.SET_DEFAULT)

    def __str__(self):
        return str(self.id)

class Faq( models.Model):
    question = models.TextField(max_length=1000)
    answer = models.TextField(max_length=1000, null=True)
    userId = models.ForeignKey(User, default=1, on_delete=models.SET_DEFAULT)

    def __str__(self):
        return str(self.id)
