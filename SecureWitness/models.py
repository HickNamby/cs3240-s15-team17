from django.db import models
from django.db.models.signals import pre_delete,post_delete, post_save
from django.dispatch.dispatcher import receiver
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager,PermissionsMixin, Group, Permission
from django.db.models.signals import pre_delete, post_delete
from django.dispatch.dispatcher import receiver
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, Group
from django.db.models import Q
import copy


import os


class SiteUserManager(BaseUserManager):
    def create_user(self, username, email, password=None):
        if not email:
            raise ValueError('Invalid Email Address')
        if not username:
            raise ValueError('Invalid Username')

        user = self.model(username=username, email=email, )
        user.is_active = True
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, email, password):
        user = self.create_user(username=username, email=email, password=password)
        user.is_staff = True
        user.is_superuser = True
        user.save()
        return user


class SiteUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(unique=True, max_length=20)
    email = models.EmailField(unique=True, max_length=225)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin_user = models.BooleanField(default=False)

    objects = SiteUserManager()
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def get_full_name(self):
        # The user is identified by their email address
        return self.email

    def get_short_name(self):
        # The user is identified by their email address
        return self.email

    def __str__(self):  # __unicode__ on Python 2
        return self.email


class Folder(models.Model):
    owner = models.ForeignKey(SiteUser, editable=False)
    title = models.CharField(max_length=50)
    ofolder = models.ManyToManyField('self')


class Report(models.Model):
    owner = models.ForeignKey(SiteUser, editable=False, related_name='owner')
    short_des = models.CharField(max_length=50)
    long_des = models.TextField()
    location = models.CharField(max_length=50)
    incident_date = models.DateTimeField()
    timestamp = models.DateTimeField(auto_now_add=True)
    keywords = models.TextField(default='report')
    public = models.BooleanField(default=True)
    folder = models.ManyToManyField(Folder)
    userviewers = models.ManyToManyField(SiteUser, related_name='userviewers')
    groupviewers = models.ManyToManyField(Group)

    def canview(self, user):
        if self.public or user == self.owner:
            return True
        if user in self.userviewers.all():
            return True
        for group in self.groupviewers.all():
            if user in group.user_set.all():
                return True
        return False

    def header(self):
        return self.short_des + " by " + self.owner.username


class File(models.Model):
    report = models.ForeignKey(Report)
    docfile = models.FileField(upload_to='documents/')

    def __str__(self):
        return self.docfile.url



@receiver(post_save, sender=SiteUser)
def update_permission(sender,instance,**kwargs):
    p1 = Permission.objects.get(codename='add_group')
    p2 = Permission.objects.get(codename='change_siteuser')
    if instance.is_admin_user:
        instance.user_permissions.add(p1)
        instance.user_permissions.add(p2)
    if not instance.is_admin_user:
        instance.user_permissions.remove(p1)
        instance.user_permissions.remove(p2)

@receiver(pre_delete, sender=File)
def file_delete(sender, instance, **kwargs):
    if instance.docfile:
        if os.path.isfile(instance.docfile.path):
            os.remove(instance.docfile.path)
