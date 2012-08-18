from django.http import HttpResponseRedirect
from gmail.forms import AccountAddForm
from django.views.generic.edit import FormView
from django.views.generic import TemplateView


class HomePageView(TemplateView):
    template_name = "gmail/homepage.html"


class AboutView(TemplateView):
    template_name = "gmail/about.html"


class AccountView(TemplateView):
    template_name = "gmail/account_detail.html"


class AccountAdd(FormView):
    template_name = 'gmail/account_create.html'
    form_class = AccountAddForm
    success_url = '/step2/'

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.

        super(AccountAdd, self).form_valid(form)
        account = form.add_account()
        profile = form.add_profile(account)
        return HttpResponseRedirect("http://127.0.0.1:8000/signup/")

        form.send_email()
        return super(AccountAdd, self).form_valid(form)


class AccountListView(TemplateView):
    template_name = "gmail/account_list.html"


class AccountChangeView(TemplateView):
    template_name = "gmail/account_change.html"
