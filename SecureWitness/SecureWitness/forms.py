from django import forms

class ReportForm(forms.Form):
	reporter = forms.CharField(label='Your name', max_length=50)
	title = forms.CharField(label='Title', max_length=50)
	docfile = forms.FileField(label='Select a file')