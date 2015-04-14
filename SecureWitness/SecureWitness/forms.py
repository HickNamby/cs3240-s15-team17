from django import forms
import datetime
from django.contrib.auth.models import User

class ReportForm(forms.Form):
	reporter = forms.CharField(label='Your name', max_length=50)
	short_des = forms.CharField(label='Summary', max_length=50)
	long_des = forms.CharField(label='Description', widget = forms.Textarea)
	location = forms.CharField(label='Location', required=False)
	date = forms.DateField(label='Date of Occurrence',initial=datetime.date.today,required=False)
	public = forms.BooleanField(label='Public',widget=forms.CheckboxInput,required=False,initial=False)

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password')