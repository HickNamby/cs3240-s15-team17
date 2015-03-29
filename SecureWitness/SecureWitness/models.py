from django.db import models

class Report(models.Model):
	reporter = models.TextField(max_length=50)
	title = models.TextField(max_length=50)
	docfile = models.FileField(upload_to='documents/%Y/%m/%d')
	def __str__(self):
		return self.reporter + " " + self.title + " " + self.docfile.url
	def header(self):
		return self.title + " by " + self.reporter