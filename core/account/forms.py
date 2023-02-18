from django import forms 
from .models import Profile

class EmailForm(forms.Form):
    email = forms.EmailField()

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ('user','follow')

