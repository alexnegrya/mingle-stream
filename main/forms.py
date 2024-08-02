from django import forms


class UserAuthForm(forms.Form):
    username = forms.CharField(required=True, min_length=1)
    password = forms.CharField(required=True, min_length=1)
