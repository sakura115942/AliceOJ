from django import forms
from django.utils.translation import ugettext_lazy as _

from .models import User


# 登陆时不能使用ModelForm，否则会因为unique冲突
class LoginForm(forms.Form):
    username = forms.CharField(max_length=32, 
                               widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Username",'autofocus': ''}))
    password = forms.CharField(max_length=64, 
                               widget=forms.PasswordInput(attrs={'class': 'form-control','placeholder': "Password"}))

# class LoginForm(forms.ModelForm):
#     class Meta:
#         model = User
#         fields = ('username', 'password', )
#         widgets = {
#             'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': "username", 'autofocus': ''}),
#             'password': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': "password"}),
#         }


class RegisterForm(forms.ModelForm):
    class Meta:
        model = User
        fields = '__all__'
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': "username", 'autofocus': ''}),
            'password': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': "password"}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': "email"}),
        }

        error_messages = {
            'username': {
                'max_length': _('The username is too long.'),
                'unique': _('The username already exist'),
            },
            'email': {
                'max_length': _("The email address is too long."),
                'unique': _('The email address is already registered'),
            }
        }
