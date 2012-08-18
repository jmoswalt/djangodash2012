from django.http import HttpResponseRedirect
from gmail.models import Account
from gmail.forms import AccountAddForm
from django.views.generic.edit import FormView
from django.views.generic import TemplateView, ListView, CreateView, DetailView, UpdateView


class HomePageView(TemplateView):
    template_name = "gmail/homepage.html"


class AboutView(TemplateView):
    template_name = "gmail/about.html"


class AccountView(DetailView):
    model = Account
    template_name = "gmail/account_detail.html"


class AccountAdd(FormView):
    template_name = 'gmail/account_create.html'
    form_class = AccountAddForm
    success_url = '/step2/'

    def form_valid(self, form):
        account = form.add_account()
        profile = form.add_profile(account)
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.

        super(AccountAdd, self).form_valid(form)
        return HttpResponseRedirect("http://127.0.0.1:8000/signup/")

        form.send_email()
        return super(AccountAdd, self).form_valid(form)


class AccountList(ListView):
    model = Account
    context_object_name = 'account'
    template_name = "gmail/account_list.html"


class AccountChange(UpdateView):
    template_name = "gmail/account_change.html"


class ClientView(DetailView):
    template_name = "gmail/client_detail.html"


class ClientAdd(CreateView):
    template_name = 'gmail/client_create.html'
    form_class = AccountAddForm
    success_url = '/step2/'

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.

        super(AccountAdd, self).form_valid(form)
        # account = form.add_account()
        # profile = form.add_profile(account)
        return HttpResponseRedirect("http://127.0.0.1:8000/signup/")

        form.send_email()
        return super(AccountAdd, self).form_valid(form)


class AccountList(ListView):
    model = Account
    context_object_name = 'account'
    template_name = "gmail/account_list.html"


class AccountChange(UpdateView):
    template_name = "gmail/account_change.html"
