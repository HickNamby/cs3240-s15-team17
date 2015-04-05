from django import forms
import datetime

class ReportForm(forms.Form):
	reporter = forms.CharField(label='Your name', max_length=50)
	short_des = forms.CharField(label='Summary', max_length=50)
	long_des = forms.CharField(label='Description', widget = forms.Textarea)
	location = forms.CharField(label='Location', required=False)
	date = forms.DateField(label='Date of Occurrence',initial=datetime.date.today,required=False)
	public = forms.BooleanField(label='Public',widget=forms.CheckboxInput,required=False,initial=False)
	docfile = forms.FileField(label='Select a file', required=False)
	encrypt_file = forms.BooleanField(label='Encrypt File(s)',widget=forms.CheckboxInput, required=False,initial=False)