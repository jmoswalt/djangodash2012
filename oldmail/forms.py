from django import forms
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

from oldmail.models import Account, Profile, SignupLink
from oldmail.utils import send_email, random_string


class AccountChangeForm(forms.ModelForm):
    name = forms.CharField()

    class Meta:
        model = Account

        fields = (
            'name',
        )

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if name:
            try:
                Account.objects.get(slug=slugify(name))
                self._errors['name'] = [_('That account name is already taken. Please pick a new one.')]
            except:
                pass
        return name

    def save_account(self):
        # Save the Account with the new name and slug
        a = self.instance
        a.name = self.cleaned_data['name']
        a.slug = slugify(self.cleaned_data['name'])
        a.save()
        return a


class AccountInviteForm(forms.ModelForm):
    #email_addresses = forms.CharField(label=_("Email Addresses"), widget=forms.Textarea, help_text=_('Add email addresses (1 per line) for people you would like to invite. They will receive an activation email.'))
    email_addresses = forms.CharField(label=_("Email Address"))

    class Meta:
        model = Account

        fields = (
            'email_addresses',
        )

    def send_invites(self):
        # Save the Account with the new name and slug
        a = self.instance
        email_addresses = self.cleaned_data['email_addresses']
        email_list = email_addresses.split('\r\n')
        site_url = settings.SITE_URL
        for email in email_list:

            if '.' in email and '@' in email:
                # generate new signup link
                signup_link = SignupLink.objects.create(random_string=random_string(60), account=a, email=email)
                message = "You've been invited to Oldmail from %s. Please click the link below to active your account. <br /><br /><a href='%s%s'>%s%s</a>" % (
                        a.name,
                        site_url,
                        signup_link.get_activate_url(),
                        site_url,
                        signup_link.get_activate_url(),
                    )
                send_email(
                    "You've been invited to Oldmail",
                    message,
                    [email]
                    )
            else:
                print "failed to validate", email
        return a


class AccountAddForm(forms.ModelForm):
    account = forms.CharField()
    email = forms.CharField()
    first_name = forms.CharField()
    last_name = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput(render_value=False))

    class Meta:
        model = User

        fields = (
            'account',
            'first_name',
            'last_name',
            'email',
            'password',
        )

    def clean_account(self):
        account = self.cleaned_data.get('account')
        if account:
            try:
                Account.objects.get(slug=slugify(account))
                self._errors['account'] = [_('That account name is already taken. Please pick a new one.')]
            except:
                pass
        return account

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email:
            try:
                User.objects.get(username=email)
                self._errors['email'] = ['That email is already taken. Do you already have an account?']
            except:
                pass
        return email

    def add_account(self):
        # Add the initial Account
        a = Account.objects.create(name=self.cleaned_data['account'], slug=slugify(self.cleaned_data['account']))
        return a

    def add_profile(self, account):
        # Add the profile
        u = User.objects.create(first_name=self.cleaned_data['first_name'],
                                last_name=self.cleaned_data['last_name'],
                                email=self.cleaned_data['email'],
                                username=self.cleaned_data['email'])
        u.set_password(self.cleaned_data['password'])
        u.save()
        p = Profile.objects.create(user=u, account=account, is_account_admin=True)
        # TODO send password_reset confirmation
        return p


class ProfileAddForm(forms.ModelForm):
    account = forms.CharField(widget=forms.HiddenInput())
    email = forms.CharField(widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    first_name = forms.CharField()
    last_name = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput(render_value=False))

    class Meta:
        model = User

        fields = (
            'email',
            'first_name',
            'last_name',
            'password',
        )

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email:
            try:
                User.objects.get(username=email)
                self._errors['email'] = ['That email is already taken. Do you already have an account?']
            except:
                pass
        return email

    def add_profile(self):
        # Add the profile
        u = User.objects.create(first_name=self.cleaned_data['first_name'],
                                last_name=self.cleaned_data['last_name'],
                                email=self.cleaned_data['email'],
                                username=self.cleaned_data['email'])
        u.set_password(self.cleaned_data['password'])
        u.save()
        p = Profile.objects.create(user=u, account_id=self.cleaned_data['account'], is_verified=True)
        # TODO send password_reset confirmation
        return p


class ProfileChangeForm(forms.ModelForm):
    email = forms.CharField(widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    password = forms.CharField(min_length=4, widget=forms.PasswordInput, required=False)

    class Meta:
        model = User

        fields = (
            'email',
            'first_name',
            'last_name',
            'password',
        )

    def __init__(self, *args, **kwargs):
        super(ProfileChangeForm, self).__init__(*args, **kwargs)

    def clean_password(self):
        password = self.cleaned_data.get('password')

        if password:  # validated (length) via form field
            self.instance.set_password(password)

        return self.instance.password
