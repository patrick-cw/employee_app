from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from .models import Employees,Salaries

class NewUserForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=20, required=True)
    last_name = forms.CharField(max_length=20, required=True)    
    class Meta:
        model = User
        fields = ("username", "email","first_name","last_name","password1", "password2")


    def save(self, commit=True):
        user = super(NewUserForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        
        if commit:
            user.save()
        return user

class EditProfileForm(UserChangeForm):
    password = None
    class Meta:
        model = User
        fields =  (
            'username',
            'email',
            'first_name',
            'last_name',
        )
        labels = {
            'username': _('Username'),
            'email': _('Email'),
            'first_name': _('First Name'),
            'last_name': _('Last Name')
        }


class DateInput(forms.DateInput):
    input_type = 'date'

class AddEmployeeForm(forms.ModelForm):
    emp_no = forms.IntegerField(required=True)
    birth_date = forms.DateField(required=True,widget=DateInput)
    first_name = forms.CharField(max_length=14,required=True)
    last_name = forms.CharField(max_length=16,required=True)
    gender = forms.CharField(max_length=1,required=True)
    hire_date = forms.DateField(required=True,widget=DateInput)
    class Meta:
        model = Employees
        fields = ("emp_no","birth_date","first_name","last_name","gender","hire_date")
    
class EditEmployeeForm(forms.ModelForm):
    birth_date = forms.DateField(required=True,widget=DateInput)
    first_name = forms.CharField(max_length=14,required=True)
    last_name = forms.CharField(max_length=16,required=True)
    gender = forms.CharField(max_length=1,required=True)
    hire_date = forms.DateField(required=True,widget=DateInput)
    class Meta:
        model = User
        fields =  (
            'birth_date',
            'first_name',
            'last_name',
            'gender',
            'hire_date',
        )
        labels = {
            'birth_date':_('Birth Date'),
            'first_name':_('First Name'),
            'last_name':_('Last Name'),
            'gender':_('Gender'),
            'hire_date':_('Hire Date'),
        }


    