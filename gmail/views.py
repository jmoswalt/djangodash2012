from django.views.generic.edit import FormView, ListView, DetailView

from gmail.forms import AccountAddForm


class AccountAdd(FormView):
    template_name = 'gmail/account_create.html'
    form_class = AccountAddForm
    success_url = '/step2/'

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        account = form.add_account()
        profile = form.add_profile(account)
        return super(AccountAdd, self).form_valid(form)
