from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import date

# Create your models here.
class CustomUser(AbstractUser):
    
    USER = (
        (1,'HOD'),
        (2,'TEACHER'),
        (3,'STUDENT'),
    )

    user_type = models.CharField(choices=USER, max_length=50, default=1)
    profile_pic = models.ImageField(upload_to='media/profile_pic')
    dob = models.DateField(max_length=8,default=date.today)
    phone_no = models.CharField(max_length=12)
    address = models.TextField()
    
class Course(models.Model):
    name = models.CharField(max_length=100)
    duration = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) 

    def __str__(self):
        return self.name


class Session_Year(models.Model):
    startSession = models.DateField()
    endSession = models.DateField()

    def __str__(self):
        return str(self.startSession) + " To " + str(self.endSession)

   
