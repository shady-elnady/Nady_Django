from django import forms
from .models import Digit
  
class DigitForm(forms.ModelForm):
  
    class Meta:
        model = Digit
        fields = ['image', 'name']