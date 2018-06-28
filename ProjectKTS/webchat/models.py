from django.contrib.auth.models import User
from django.db import models
from django.conf import settings
import os
 
class Profile(models.Model):
    user = models.OneToOneField(User,on_delete = models.CASCADE)
    
    # avatar = models.ImageField(upload_to='image/%Y/%m/%d', default = os.path.join(settings.MEDIA_ROOT, 'image/2018/01/23/user.png'), blank=True, null=True)

    def __str__(self):
        return self.user.username

class Rooms(models.Model):
    
    users = models.ManyToManyField(Profile)
    admin = models.ForeignKey(Profile,related_name='admin', on_delete = models.SET_NULL, null = True)
    create_date = models.DateTimeField(auto_now_add = True)
    name = models.CharField(max_length=128)
    # img = models.ImageField(upload_to='image/%Y/%m/%d', default = os.path.join(settings.MEDIA_ROOT, 'image/2018/01/23/user.png'), blank=True, null=True)

    def __str__(self):
        return self.name  

class Message(models.Model):
    author = models.ForeignKey(Profile, on_delete = models.SET_NULL, null = True)
    text = models.TextField()
    date_pubs = models.DateTimeField(auto_now_add = True)
    room = models.ForeignKey(Rooms, on_delete = models.CASCADE)


    def __str__(self):
        return self.text 

class Invite(models.Model):
    room = models.ForeignKey(Rooms, on_delete=models.CASCADE)
    recipient = models.ForeignKey(Profile, on_delete=models.CASCADE)
    sender = models.ForeignKey(Profile, related_name='sender', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.room.name
# Create your models here.
