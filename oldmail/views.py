import urllib
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.views.generic.edit import FormView
from django.views.generic import TemplateView
from django.conf import settings
from django.http import Http404
from django.template import RequestContext
from django.shortcuts import render_to_response
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
        messages.success(self.request, 'Successfully added a profile: %s.' % profile.user.get_full_name(), extra_tags='success')
        return HttpResponseRedirect(reverse('homepage'))


class AccountListView(TemplateView):
    template_name = "account_list.html"


class AccountChangeView(TemplateView):
    template_name = "account_change.html"
    
#@login_required
def authenticate(request, template_name = 'authenticate.html'):
    """
    Authenticate a user with his/her gmail account. 
    
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
    pass
    
