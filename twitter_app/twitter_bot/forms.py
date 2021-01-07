from django import forms
from django.forms import CharField


class InputForm(forms.Form):
    user_input = forms.CharField(label='Username', max_length=100)
