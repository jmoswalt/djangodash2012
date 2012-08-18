from django import forms
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify

from gmail.models import Account, Profile


class AccountAddForm(forms.ModelForm):
    account_name = forms.CharField()
    email = forms.CharField()
    first_name = forms.CharField()
    last_name = forms.CharField()

    class Meta:
        model = Account

        fields = (
            'first_name',
            'last_name',
            'email',
            'account_name',
        )

    def add_account(self):
        # Add the initial Account
        a = Account.objects.create(name=self.account_name, slug=slugify(self.account_name))
        return a

    def add_profile(self, account):
        # Add the profile
        u = User.objects.create(first_name=self.first_name,
                                last_name=self.last_name,
                                email=self.email)
        p = Profile.objects.create(user=u, account=self.account)
        # TODO send password_reset confirmation
        return p
