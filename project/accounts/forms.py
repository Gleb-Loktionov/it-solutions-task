from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import password_validation


class RegisterForm(UserCreationForm):
    password1 = forms.CharField(
        label="Пароль",
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password', 'class': 'form-control mb-3'}),
        help_text=password_validation.password_validators_help_text_html(),
    )
    password2 = forms.CharField(
        label="Подтверждение пароля",
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password', 'class': 'form-control mb-3'}),
        strip=False,
        help_text="Введите такой же пароль как в поле выше",
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = [
            'username', 'first_name', 'last_name',
            'email', 'password1', 'password2'
        ]

        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control mb-3'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control mb-3'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control mb-3'}),
            'email': forms.EmailInput(attrs={'class': 'form-control mb-3'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control mb-3'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control mb-3'}),
        }


class LoginForm(AuthenticationForm):
    username = forms.CharField(max_length=100 , widget=forms.TextInput(attrs={
                'class': 'form-control mb-3'
            }
        )
    )
    password = forms.CharField(max_length=100, label='Пароль', widget=forms.PasswordInput(attrs={
                'class': 'form-control mb-3'
            }
        )
    )