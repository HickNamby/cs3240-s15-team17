from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin
from django import forms
from SecureWitness.models import Report, SiteUser, SiteUserManager
from django.contrib.auth.forms import ReadOnlyPasswordHashField

class UserCreationForm(forms.ModelForm):

    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = SiteUser
        fields = ('email',)

    def clean_password2(self):

        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):

        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

class UserChangeForm(forms.ModelForm):

    password = ReadOnlyPasswordHashField()

    class Meta:
        model = SiteUser
        fields = ('email', 'password', 'is_active')

    # def clean_password(self):

    #     return self.initial["password"]


class SiteUserAdmin(UserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ('username','email','is_staff','is_superuser')
    list_filter = ('is_superuser',)

    fieldsets = (
        (None,{'fields':('username','email','password')}),('Permissions',{'fields':('is_active','is_superuser','is_staff','is_admin_user','groups','user_permissions')})
    )


admin.site.register(Report)
admin.site.register(SiteUser,SiteUserAdmin)
