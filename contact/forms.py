from django.forms import ModelForm
from .models import Contact
from django import forms

class ContactForm(ModelForm):
    class Meta:
        model = Contact
        fields = ['name', 'email', 'phone', 'message']
        widgets = {
            field: forms.TextInput(
                attrs={
                'class': "form-control",
                'placeholder': field.capitalize()
                }
            )
            for field in fields
        }