import urllib
import urllib2
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth import authenticate as dj_auth
from django.views.generic import TemplateView, DetailView, ListView
from django.views.generic.edit import FormView, UpdateView, CreateView
from django.conf import settings
from django.http import Http404
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from django.utils import simplejson
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from oldmail.utils import lazy_reverse
from oldmail.models import Account, Client, SignupLink, Profile, Contact
from oldmail.forms import AccountAddForm, AccountChangeForm, AccountInviteForm, ProfileAddForm
from oldmail.decorators import staff_or_super_required
from oldmail.utils import send_email, random_string


class HomePageView(TemplateView):
    template_name = "home.html"


class AboutView(TemplateView):
    template_name = "about.html"


class AccountView(DetailView):
    model = Account
    template_name = "account_detail.html"

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(AccountView, self).dispatch(*args, **kwargs)

    def get_object(self, **kwargs):
        user = self.request.user
        obj = get_object_or_404(Account, slug=self.kwargs['slug'])
        # Check if you can see this object
        if not user.is_staff and not user.is_superuser:
            if not user.profile.account == obj:
                raise Http404
        return obj


class AccountAdd(FormView):
    template_name = 'account_create.html'
    form_class = AccountAddForm

    def form_valid(self, form):
        account = form.add_account()
        profile = form.add_profile(account)
        user = dj_auth(username=profile.user.username, password=form.cleaned_data['password'])
        login(self.request, user)
        messages.success(self.request, 'Your account for %s has been created. You are now logged in.' % account.name, extra_tags='success')
        return HttpResponseRedirect(reverse('account_detail', args=[account.slug]))


class AccountListView(ListView):
    model = Account
    template_name = "account_list.html"

    @method_decorator(staff_or_super_required)
    def dispatch(self, *args, **kwargs):
        return super(AccountListView, self).dispatch(*args, **kwargs)


class AccountInviteView(UpdateView):
    template_name = "account_invite.html"
    form_class = AccountInviteForm

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(AccountInviteView, self).dispatch(*args, **kwargs)

    def get_object(self, **kwargs):
        user = self.request.user
        if not user.profile.is_account_admin:
            raise Http404
        obj = get_object_or_404(Account, slug=self.kwargs['slug'])
        # Check if you can see this object
        if not user.is_staff and not user.is_superuser:
            if not user.profile.account == obj:
                raise Http404
        if not user.profile.is_verified:
            site_url = settings.SITE_URL
            signup_link = SignupLink.objects.create(random_string=random_string(60), account=obj, email=user.email)
            message = "You've been invited to Oldmail from %s. Please click the link below to active your account. <br /><br /><a href='%s%s'>%s%s</a>" % (
                    obj.name,
                    site_url,
                    signup_link.get_verify_url(),
                    site_url,
                    signup_link.get_verify_url(),
                )
            send_email(
                "Please validate your Oldmail account",
                message,
                [user.email]
                )
        return obj

    def form_valid(self, form):
        account = form.send_invites()
        return HttpResponseRedirect(reverse('account_detail', args=[account.slug]))


class AccountChangeView(UpdateView):
    template_name = "account_change.html"
    form_class = AccountChangeForm

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(AccountChangeView, self).dispatch(*args, **kwargs)

    def get_object(self, **kwargs):
        user = self.request.user
        obj = get_object_or_404(Account, slug=self.kwargs['slug'])
        # Check if you can see this object
        if not user.is_staff and not user.is_superuser:
            if not user.profile.account == obj:
                raise Http404
        return obj

    def form_valid(self, form):
        account = form.save_account()
        return HttpResponseRedirect(reverse('account_detail', args=[account.slug]))


class ProfileAddView(FormView):
    template_name = 'profile_add.html'
    form_class = ProfileAddForm

    def get_initial(self):
        initial = super(ProfileAddView, self).get_initial()
        signup_link = get_object_or_404(SignupLink, random_string=self.kwargs['random_string'], account__slug=self.kwargs['slug'])
        initial['account'] = signup_link.account_id
        print signup_link.email
        initial['email'] = signup_link.email
        return initial

    def form_valid(self, form):
        profile = form.add_profile()
        user = dj_auth(username=profile.user.username, password=form.cleaned_data['password'])
        login(self.request, user)
        messages.success(self.request, 'Your profile for %s has been created. You are now logged in.' % profile.account.name, extra_tags='success')
        return HttpResponseRedirect(reverse('account_detail', args=[profile.account.slug]))


class ProfileVerifyView(DetailView):
    template_name = 'profile_add.html'
    model = Profile

    def get_object(self, **kwargs):
        signup_link = get_object_or_404(SignupLink, random_string=self.kwargs['random_string'], account__slug=self.kwargs['slug'])
        profile = get_object_or_404(Profile, user__email=signup_link.email)
        profile.is_verified = True
        profile.save()

        return profile

    def render_to_response(self, context):
        return HttpResponseRedirect(reverse('account_invite', args=[self.get_object().account.slug]))



#@login_required
def authenticate(request, template_name = 'authenticate.html'):
    """
    Authenticate a user with his/her gmail account. 
    The user can grant or denied the access.
    
    access_type: online or offline
    approval_prompt: force or auto
    """
    # construct the url to authenticate
    if not all([hasattr(settings, 'OAUTH2_CLIENT_ID'),
                hasattr(settings, 'OAUTH2_REDIRECT_URL')]):
        raise Http404
    
    if request.method == "POST":
        url = settings.OAUTH2_ENDPOINT
        params = {'scope': settings.OAUTH2_SCOPE,
                  'client_id': settings.OAUTH2_CLIENT_ID,
                  'redirect_uri': settings.OAUTH2_REDIRECT_URL,
                  'response_type': 'code',
                  'state': '',
                  'access_type': 'offline',
                  'approval_prompt': 'auto'} 
        #TODO: assign user to the state param
        url = '%s?%s' % (url, urllib.urlencode(params))
        
        return HttpResponseRedirect(url)
    
    return render_to_response(template_name, {'folder_name': 
                                       settings.CLIENT_FOLDER_NAME},
            context_instance=RequestContext(request))


def authenticate_callback(request):
    """
    Handle the response after the auth request gets sent back to the site.
    """
    # first, get the authorization code.
    error = request.GET.get('error', '')
    if error == 'access_denied':
        # redirect to let them try again
        messages.add_message(request, messages.ERROR, 'Access denied.')
        return HttpResponseRedirect(reverse('authenticate'))

    code = request.GET.get('code', '')
    state = request.GET.get('state', '')

    # exachange the authorization code for an access token and a refresh token
    params = {'code': code,
              'client_id': settings.OAUTH2_CLIENT_ID,
              'client_secret': settings.OAUTH2_CLIENT_SECRET,
              'redirect_uri': settings.OAUTH2_REDIRECT_URL,
              'grant_type': 'authorization_code'}
    result = urllib2.urlopen('http://example.com', urllib.urlencode(params))
    content = result.read()

    # a successful response is returned as a JSON array
    content_d = simplejson.loads(content)
    access_token = content_d['access_token']
    expires_in = content_d['expires_in']
    token_type = content_d['token_type']
    refresh_token = content_d['refresh_token']


class ClientCreate(CreateView):
    model = Client
    template_name = 'client_form.html'

    def get_success_url(self):
        return lazy_reverse('client_list', self.request.user.profile.account.slug)


class ClientList(ListView):
    model = Client
    template_name = 'client_list.html'


class ClientChange(UpdateView):
    model = Client
    template_name = 'client_form.html'

    def get_success_url(self):
        return lazy_reverse('client_list', self.request.user.profile.account.slug)


class ContactCreate(CreateView):
    model = Contact
    template_name = 'contact_form.html'

    def get_success_url(self):
        return lazy_reverse('contact_list', self.request.user.profile.account.slug)


class ContactList(ListView):
    model = Contact
    template_name = 'contact_list.html'


class ContactChange(UpdateView):
    model = Contact
    template_name = 'contact_form.html'

    def get_success_url(self):
        return lazy_reverse('contact_list', self.request.user.profile.account.slug)


class ProfileList(ListView):
    model = Profile
    template_name = 'profile_list.html'


class ProfileChange(UpdateView):
    model = Profile
    template_name = 'profile_form.html'

    def get_success_url(self):
        return lazy_reverse('profile_list', self.request.user.profile.account.slug)
