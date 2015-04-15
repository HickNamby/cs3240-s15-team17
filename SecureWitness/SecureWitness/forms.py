from django import forms
import datetime
from django.contrib.auth.models import User

class ReportForm(forms.Form):
	short_des = forms.CharField(label='Summary', max_length=50)
	long_des = forms.CharField(label='Description', widget = forms.Textarea)
	location = forms.CharField(label='Location', required=False)
	date = forms.DateField(label='Date of Occurrence',initial=datetime.date.today,required=False)
	public = forms.BooleanField(label='Public',widget=forms.CheckboxInput,required=False,initial=False)

class FolderForm(forms.Form):
	title = forms.CharField(label='Folder Name:',max_length=50)

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password')