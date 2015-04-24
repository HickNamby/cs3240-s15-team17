from django import forms
import datetime

class ReportForm(forms.Form):
	short_des = forms.CharField(label='Summary', max_length=50)
	long_des = forms.CharField(label='Description', widget = forms.Textarea)
	location = forms.CharField(label='Location', required=False)
	date = forms.DateField(label='Date of Occurrence',initial=datetime.date.today,required=False)
	keywords = forms.CharField(label='Keywords (separate with commas):',widget=forms.Textarea)
	public = forms.BooleanField(label='Public',widget=forms.CheckboxInput,required=False,initial=False)

class FolderForm(forms.Form):
	title = forms.CharField(label='Folder Name:',max_length=50)

class UserForm(forms.Form):
	username = forms.CharField(max_length=50)
	email = forms.EmailField(max_length=50)
	password = forms.CharField(widget=forms.PasswordInput())

class GroupForm(forms.Form):
    name = forms.CharField(max_length=50)

class SearchForm(forms.Form):
    searchText = forms.CharField(label='Search:', max_length=100, required=True)