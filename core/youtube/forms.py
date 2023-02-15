from django import forms
from .models import Video ,VideoTag

class VideoEditForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ['title','description','thumbnail','monetize','tags','category']
    
    tags = forms.ModelMultipleChoiceField(
        queryset=VideoTag.objects.all(),
        widget=forms.CheckboxSelectMultiple(attrs={'style':'width : unset ; height : unset'})
    )