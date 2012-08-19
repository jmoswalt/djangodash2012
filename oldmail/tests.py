"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from django.test.client import Client

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
        
    def test_account_login(self):
        client = Client()
        response = client.get('/accounts/login/')
        self.assertEqual(response.status_code, 200)
        
    def test_account_out(self):
        client = Client()
        response = client.get('/accounts/logout/')
        self.assertEqual(response.status_code, 200)
        
    def test_about(self):
        client = Client()
        response = client.get('/about/')
        self.assertEqual(response.status_code, 200)
        
    def test_signup(self):
        client = Client()
        response = client.get('/signup/')
        self.assertEqual(response.status_code, 200)
        
    def test_home(self):
        client = Client()
        response = client.get('/')
        self.assertEqual(response.status_code, 200)
