from django import forms
from django.core.validators import EmailValidator


class ContactForm(forms.Form):
    first_name = forms.CharField(max_length=100, required=True)
    last_name = forms.CharField(max_length=100, required=True)
    email = forms.CharField(validators=[EmailValidator()], required=True)
    phone = forms.CharField(max_length=15, required=False)
    message = forms.CharField(widget=forms.Textarea, required=True)