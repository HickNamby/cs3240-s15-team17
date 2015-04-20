from django.db import models
from django.db.models.signals import pre_delete,post_delete
from django.dispatch.dispatcher import receiver
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager,PermissionsMixin

import os

class SiteUserManager(BaseUserManager):

    def create_user(self, username, email, password = None):
        if not email:
            raise ValueError('Invalid Email Address')
        if not username:
            raise ValueError('Invalid Username')

        user = self.model(username=username, email=email,)
        user.is_active = True
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self,username,email,password):
        user = self.create_user(username=username,email=email,password=password)
        user.is_staff = True
        user.is_superuser = True
        user.save()
        return user

class SiteUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(unique=True, max_length=20)
    email = models.EmailField(unique=True,max_length=225)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin_user = models.BooleanField(default=False)

    objects = SiteUserManager()
    USERNAME_FIELD = 'username'


    def get_full_name(self):
        # The user is identified by their email address
        return self.email

    def get_short_name(self):
        # The user is identified by their email address
        return self.email

    def __str__(self):              # __unicode__ on Python 2
        return self.email



class Folder(models.Model):
	owner = models.ForeignKey(SiteUser, editable=False)
	title = models.CharField(max_length=50)
	ofolder = models.ManyToManyField('self')

class Report(models.Model):
	owner = models.ForeignKey(SiteUser, editable=False)
	short_des = models.CharField(max_length=50)
	long_des = models.TextField()
	location = models.CharField(max_length=50)
	incident_date = models.DateTimeField()
	timestamp = models.DateTimeField(auto_now_add=True)
	public = models.BooleanField(default=True)
	folder = models.ManyToManyField(Folder)
	def header(self):
		return self.owner.username + " " + self.short_des + " " + self.long_des + " " + self.location + " " + str(self.incident_date) + " " + str(self.timestamp) + " " + str(self.public)

class File(models.Model):
	report = models.ForeignKey(Report)
	docfile = models.FileField(upload_to='documents/')
	def __str__(self):
		return self.docfile.url

@receiver(pre_delete, sender=File)
def file_delete(sender,instance,**kwargs):
	if instance.docfile:
		if os.path.isfile(instance.docfile.path):
			os.remove(instance.docfile.path)

