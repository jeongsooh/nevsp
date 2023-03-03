from django import forms
from .models import Variables

class VariablesUpdateForm(forms.ModelForm):
    class Meta:
        model = Variables
        fields = ['group','interval']
