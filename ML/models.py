from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
# Create your models here.

class Users(models.Model):
    STANDARD = (
            (0,"other"),(1,"STD-I"),(2,"STD-II"),(3,"STD-III"),
            (4,"STD-IV"),(5,"STD-V"),(6,"STD-VI"),(7,"STD-VII"),
            (8,"STD-VIII"),(9,"STD-IX"),(10,"STD-X"),(11,"STD-XI"),
            (12,"STD-XII"))
    GENDER = ((1,"F"),(2,"M"))
    name = models.CharField(max_length=25)
    surname = models.CharField(max_length=25)
    gender = models.IntegerField(choices=GENDER)
    age = models.IntegerField()
    standard = models.IntegerField(choices=STANDARD)
    school_name = models.CharField(max_length=100)
    pincode = models.CharField(max_length=20)
    users = models.OneToOneField(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return '''Users(name={}, surname={}, gender={}, age={}, standard={}, school_name={}, pincode={})'''.format(self.name, self.surname, self.gender, self.age, self.standard, self.school_name, self.pincode)

class Notes(models.Model):

    author = models.ForeignKey('auth.User', on_delete=None)
    notes = models.TextField(default='')
    date = models.DateTimeField(auto_now_add=True)
    types = models.CharField(max_length=20)



    def saved_date(self):
        self.date = timezone.now()
        self.save()

    def snippest(self):
        return self.notes[:50]+'...'

class UserActivityPath(models.Model):
    user = models.ForeignKey('auth.User', on_delete=None)
    date = models.DateTimeField(auto_now_add=True)
    seeking = models.IntegerField(default = 0)
    pauses = models.IntegerField(default = 0)
    replaycount = models.IntegerField(default = 0)
    path = models.CharField(max_length=100)


    def saved_date(self):
        self.date = timezone.now()
        self.save()

    def __str__(self):
        return '''UserActivity(user={},date={}, seeking={}, pauses={}, replaycount={}, path={})'''.format(self.user,self.date, self.seeking, self.pauses, self.replaycount, self.path)


class Questions(models.Model):
    user = models.ForeignKey('auth.User',on_delete=None)
    date = models.DateTimeField(auto_now_add=True)
    basic = models.IntegerField(default=0)
    intermediate=models.IntegerField(default=0)
    advance=models.IntegerField(default=0)
    avg = models.IntegerField(default=0)
