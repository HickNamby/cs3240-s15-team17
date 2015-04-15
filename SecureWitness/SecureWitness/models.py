from django.db import models
from django.db.models.signals import pre_delete,post_delete
from django.dispatch.dispatcher import receiver
from django.contrib.auth.models import User

import os


class Folder(models.Model):
	owner = models.ForeignKey(User, editable=False)
	title = models.CharField(max_length=50)
	ofolder = models.ManyToManyField('self')

class Report(models.Model):
	owner = models.ForeignKey(User, editable=False)
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