from django import forms
from .models import Subscriber


class ContactForm(forms.Form):
    name = forms.CharField(max_length=100, required=False)
    email = forms.EmailField(required=True)
    subject = forms.CharField(max_length=100, required=True)
    message = forms.CharField(max_length=250, required=False)


class SubscribeForm(forms.ModelForm):
    class Meta:
        model = Subscriber
        fields = ("name", "email")
