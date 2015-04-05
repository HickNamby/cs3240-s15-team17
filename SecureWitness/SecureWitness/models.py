from django.db import models
from django.db.models.signals import pre_delete,post_delete
from django.dispatch.dispatcher import receiver
import os

class Report(models.Model):
	reporter = models.CharField(max_length=50)
	short_des = models.CharField(max_length=50)
	long_des = models.TextField()
	location = models.CharField(max_length=50)
	incident_date = models.DateTimeField()
	timestamp = models.DateTimeField(auto_now_add=True)
	public = models.BooleanField(default=True)
	#keywords (how????)
	def header(self):
		return self.reporter + " " + self.short_des + " " + self.long_des + " " + self.location + " " + str(self.incident_date) + " " + str(self.timestamp) + " " + str(self.public)

class File(models.Model):
	report = models.ForeignKey(Report)
	encrypt_file = models.BooleanField(default=False)
	docfile = models.FileField(upload_to='documents/')
	def __str__(self):
		return self.docfile.url

@receiver(pre_delete, sender=File)
def file_delete(sender,instance,**kwargs):
	if instance.docfile:
		if os.path.isfile(instance.docfile.path):
			os.remove(instance.docfile.path)