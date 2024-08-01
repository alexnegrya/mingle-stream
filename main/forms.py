from django import forms


class UserAuthForm(forms.Form):
    username = forms.CharField(required=True)
    password = forms.CharField(required=True)
