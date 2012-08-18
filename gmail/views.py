from django.views.generic.edit import FormView

from gmail.forms import AccountAddForm


class AccountAdd(FormView):
    template_name = 'gmail/account_create.html'
    form_class = AccountAddForm
    success_url = '/step2/'

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        form.send_email()
        return super(AccountAdd, self).form_valid(form)
