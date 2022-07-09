from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from accounts.models import UserAccount

User = get_user_model()


class RegisterUserForm(UserCreationForm):
    password1 = forms.CharField(max_length=50, label='Password',
                                required=True,
                                widget=forms.PasswordInput(attrs={'placeholder': 'Password',
                                                                  'class': 'form-control',
                                                                  'data-toggle': 'password',
                                                                  'id': 'password',
                                                                  }))
    password2 = forms.CharField(max_length=50, label='Confirm Password',
                                required=True,
                                widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password',
                                                                  'class': 'form-control',
                                                                  'data-toggle': 'password',
                                                                  'id': 'password',
                                                                  }))

    class Meta:
        model = User
        fields = ['email', 'username', 'first_name', 'last_name']

        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control signup-email', 'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control signup-email', 'placeholder': 'Last Name'}),
            'email': forms.TextInput(
                attrs={'class': 'form-control signup-email', 'type': 'email', 'placeholder': 'Email'}),
            'username': forms.TextInput(
                attrs={'class': 'form-control signup-email', 'placeholder': 'Username'}),
            # 'role': forms.Select(attrs={'class': 'form-control signup-email', 'label': 'Role'}),
        }


class UserAccountForm(forms.ModelForm):
    class Meta:
        model = UserAccount
        fields = ['about', 'role','profile_photo']

        widgets = {
            'role': forms.TextInput(attrs={'class': 'form-control', 'readonly': True}),
            'about': forms.Textarea(attrs={'class': 'form-control'}),
            'profile_photo':forms.FileInput(),
        }