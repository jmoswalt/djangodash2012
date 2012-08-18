from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.views.generic.edit import FormView
from django.views.generic import TemplateView

from oldmail.forms import AccountAddForm


class HomePageView(TemplateView):
    template_name = "home.html"


class AboutView(TemplateView):
    template_name = "oldmail/about.html"


class AccountView(TemplateView):
    template_name = "oldmail/account_detail.html"


class AccountAdd(FormView):
    template_name = 'oldmail/account_create.html'
    form_class = AccountAddForm

    def form_valid(self, form):
        account = form.add_account()
        profile = form.add_profile(account)
        # TODO Redirect to the profile detail page
        messages.success(self.request, 'Successfully added a profile: %s.' % profile.user.get_full_name(), extra_tags='success')
        return HttpResponseRedirect(reverse('homepage'))


class AccountListView(TemplateView):
    template_name = "oldmail/account_list.html"


class AccountChangeView(TemplateView):
    template_name = "oldmail/account_change.html"
