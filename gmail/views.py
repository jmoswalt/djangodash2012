from django.views.generic import CreateView
from django.http import HttpResponseRedirect

from gmail.forms import AccountAddForm


class AccountAdd(CreateView):
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
