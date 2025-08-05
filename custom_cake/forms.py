from django import forms
from .models import CustomCake

class CustomCakeForm(forms.ModelForm):
    class Meta:
        model = CustomCake
        fields = ['name', 'occasion', 'flavor', 'size', 'inscription', 'description', 'image']
