from django import forms


class AccountAddForm(forms.Form):
    name = forms.CharField()
    email = forms.CharField()
