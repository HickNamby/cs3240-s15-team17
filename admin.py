from django.contrib.admin.sites import AdminSite
from SecureWitness.models import SiteUser
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin, admin
from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from django.contrib.auth.forms import AuthenticationForm

class UserAdminSite(AdminSite):
    site_header = "SecureWitness Admin Site"
    site_title = "Manage User and Groups"
    login_form = AuthenticationForm

    def has_permission(self, request):
        return request.user.is_active and request.user.is_admin_user

user_admin = UserAdminSite(name="UserAdmin")

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
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = SiteUser
        fields = ('email', 'password', 'is_active')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]

class SiteUserAdmin(UserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ('username','email',)
    list_filter = ('is_superuser',)

    fieldsets = (
        (None,{'fields':('username','email','password')}),('Permissions',{'fields':('is_active','is_admin_user','groups')})
    )

class SiteGroupAdmin(admin.ModelAdmin):

    readonly_fields = ['permissions']

user_admin.register(SiteUser,SiteUserAdmin)
user_admin.register(Group,SiteGroupAdmin)
