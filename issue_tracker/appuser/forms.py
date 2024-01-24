from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from .models import AppUser


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='Username',
                               widget=forms.TextInput(attrs=
                                                      {'type': 'text',
                                                       'class': 'form-control',
                                                       'placeholder': 'Username',
                                                       'id': 'Username',
                                                       }
                                                      )
                               )
    password = forms.CharField(label='Password',
                               widget=forms.TextInput(attrs=
                                                      {'type': 'password',
                                                       'class': 'form-control',
                                                       'placeholder': 'Password',
                                                       'id': 'Password'}
                                                      )
                               )