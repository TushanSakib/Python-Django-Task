from django.db import models
from django.contrib.auth.models import User
from datetime import date
# Create your models here.
class Vanue(models.Model):
    name = models.CharField(max_length=300)
    address = models.CharField(max_length=120)
    zip_code = models.CharField(max_length=20)
    phone = models.CharField(max_length=12,blank=True)
    web = models.URLField('Website Address',blank=True)
    email_address = models.EmailField('Email Address',blank=True)
    vanue_image = models.ImageField(null=True,blank=True,upload_to="images/")
    owner = models.IntegerField("Venue Owner",blank=False,default=1)

    def __str__(self):
        return self.name

class MyClubUser(models.Model):
    first_name = models.CharField(max_length=120)
    last_name = models.CharField(max_length=120)
    email = models.EmailField('User Email')

    def __str__(self):
        return self.first_name+ ' '+self.last_name

class Event(models.Model):
    name = models.CharField('Event Name',max_length=120)
    event_date = models.DateTimeField('Event Date')
    vanue = models.ForeignKey(Vanue,blank=True,null=True,on_delete = models.CASCADE)
    #venue = models.CharField(max_length=120)
    manager = models.ForeignKey(User,blank=True,null=True,on_delete=models.SET_NULL)
    description = models.TextField(blank=True)
    attendees = models.ManyToManyField(MyClubUser,blank=True)
    approved = models.BooleanField("Approved",default=False)


    def __str__(self):
        return self.name

    @property
    def Days_till(self):
        today = date.today()
        days_till = self.event_date.date() - today
        if self.event_date.date() < today:
            days_till_stripped = "Past"
        else:
            days_till_stripped = str(days_till).split(",",1)[0]
        return days_till_stripped


