from django.forms import ModelForm
from .models import Contact,Post

class ContactForm(ModelForm):
    class Meta:
        model=Contact
        fields='__all__'

class PostForm(ModelForm):
    class Meta:
        model=Post
        exclude=("owner","view_count","slug")