from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django import forms
from django.contrib.auth.forms import AuthenticationForm, UsernameField

from services.forms import FormStyleMixin
from users.models import User


class UserLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)

    username = UsernameField(
        widget=forms.TextInput(
            attrs={
                'class': 'mdl-textfield__input',
                'placeholder': 'Email',
                'id': 'login-email'
            }
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'mdl-textfield__input',
                'placeholder': 'Password',
                'id': 'login-password',
            }
        )
    )


class UserForm(FormStyleMixin, UserChangeForm):
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'phone', 'country', 'avatar')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password'].widget = forms.HiddenInput()


class UserRegisterForm(FormStyleMixin, UserCreationForm):
    class Meta:
        model = User
        fields = ('email', 'password1', 'password2')
