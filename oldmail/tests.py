"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase


class SimpleTest(TestCase):

    def setUp(self):
        """
        Create list of accounts. (self.accounts)
        """
        from django.contrib.auth.models import User
        from django.template.defaultfilters import slugify
        from oldmail.models import Account, Profile, Client, Contact

        account_name = 'Schipul'
        self.account = Account.objects.create(
                name=account_name,
                slug=slugify(account_name)
            )

        self.user = User.objects.create_user(
            'tyler_durden',
            'tyler_durden@gmail.com',
            'tylers_password_is_not_safe',
        )

        self.profile = Profile.objects.create(
            account=self.account,
            user=self.user
        )

        self.client = Client.objects.create(
            name='Paper Company',
            account=self.account,
        )

        self.contact = Contact.objects.create(
            client=self.client,
            account=self.account,
            name='Bob Hope',
            email='hope@gmail.com'
        )

    def test_data_retrieval(self):
        from oldmail.models import Account, Profile, Client, Contact

        print 'Testing data creation/retrieval'

        print '%d Account' % Account.objects.count()
        print '%d Profile' % Profile.objects.count()
        print '%d Client' % Client.objects.count()
        print '%d Contact' % Contact.objects.count()
