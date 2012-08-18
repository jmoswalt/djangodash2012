import urllib, urllib2
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth import authenticate as dj_auth
from django.views.generic.edit import FormView
from django.views.generic import TemplateView
from django.conf import settings
from django.http import Http404
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse
from django.utils import simplejson
from django.contrib.auth.decorators import login_required

from oldmail.forms import AccountAddForm


class HomePageView(TemplateView):
    template_name = "home.html"


class AboutView(TemplateView):
    template_name = "about.html"


class AccountView(TemplateView):
    template_name = "account_detail.html"


class AccountAdd(FormView):
    template_name = 'account_create.html'
    form_class = AccountAddForm

    def form_valid(self, form):
        account = form.add_account()
        profile = form.add_profile(account)
        # TODO Redirect to the profile detail page
        user = dj_auth(username=profile.user.username, password=form.cleaned_data['password'])
        login(self.request, user)
        messages.success(self.request, 'Your account for %s has been created. You are now logged in.' % account.name, extra_tags='success')
        return HttpResponseRedirect(reverse('homepage'))


class AccountListView(TemplateView):
    template_name = "account_list.html"


class AccountChangeView(TemplateView):
    template_name = "account_change.html"
    
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
    

    
