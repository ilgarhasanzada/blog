from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django import forms

User=get_user_model()
def validate_email(value):
    if User.objects.filter(email = value).exists():
        raise ValidationError(
            (f"{value} is taken."),
            params = {'value':value}
        )
class RegisterForm(UserCreationForm):
    email = forms.EmailField(validators = [validate_email],widget=forms.EmailInput(
                attrs = {
                    'class': 'form-control',
                    'placeholder': 'Email'
                }))
    class Meta:
        model = User
        fields=("username", "email", "first_name", "last_name")
        widgets={
            'username':forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Username'
                }
            ),
            "first_name": forms.TextInput(
                attrs = {
                    'class': 'form-control',
                    'placeholder': 'First Name'
                }
            ),
            "last_name": forms.TextInput(
                attrs = {
                    'class': 'form-control',
                    'placeholder': 'Last Name'
                }
            )
        }
