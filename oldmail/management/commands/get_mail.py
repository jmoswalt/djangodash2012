from dateutil.parser import parse
import re

from django.core.management.base import BaseCommand
from django.shortcuts import get_object_or_404

from oldmail.models import Profile, Message, Contact


class Command(BaseCommand):
    """
    Get mail for a Profile

    Needs 1 arg, the email address for the associated profile
    """
    def get_contact(self, to_email_addr, from_email_addr, profile):
        c = None
        # First we check if the to address is the client.
        to_email = re.sub("(.*)<([\\w\\-\\.\\@]+)>", "\\2", to_email_addr).split(',')[0]
        to_name = ''
        if "<" in to_email_addr:
            to_name = to_email_addr.split("<")[0].rstrip().replace("'", '').replace('"', '').replace('=?utf-8?Q?', '').replace('?=', '').replace('=20', ' ')
        # make sure the address is not the sender
        if to_email != profile.user.email:
            try:
                c = Contact.objects.get(email=to_email, account=profile.account)
                return c
            except:
                c = Contact.objects.create(email=to_email, name=to_name, account=profile.account)
                return c

        # now we check the from
        from_email = re.sub("(.*)<([\\w\\-\\.\\@]+)>", "\\2", from_email_addr).split(',')[0]
        from_name = ''
        if "<" in from_email_addr:
            from_name = from_email_addr.split("<")[0].rstrip().replace("'", '').replace('"', '').replace('=?utf-8?Q?', '').replace('?=', '').replace('=20', ' ')
        if from_email != profile.user.email:
            try:
                c = Contact.objects.get(email=from_email, account=profile.account)
                return c
            except:
                c = Contact.objects.create(email=from_email, name=from_name, account=profile.account)
                return c

        # to email and from email are same as profile_email
        if to_email == from_email:
            c = Contact.objects.create(email=from_email, account=profile.account)
            return c

    def parse_address(self, address):
        result = re.sub("(.*)<([\\w\\.\\@]+)>", "\\2", address)
        return result.split(',')[0].lower()

    def parse_subject(self, subject):
        result = subject.replace('=20', ' ').replace('=?UTF-8?Q?', '').replace('=?utf-8?Q?', '').replace('?=', '').replace('=27', "'").replace('=E2=80=99', "'")
        return result

    def parse_body(self, body):
        result = body.replace('=\r\n', '').replace('=\n\r', '')
        if "<html>" in body:
            result = result.replace('\r', '').replace('\n', '')
        result = result.replace('=3D', '=').replace('=20', ' ').replace('=0D', '')
        result = result.replace("=90", '').replace("=09", '')
        result = result.replace('=C2=A0', ' ').replace('=E2=80=99', "'")
        result = result.replace('=0A', '')
        return result

    def handle(self, *args, **options):
        try:
            email_address = args[0]
            profiles = [get_object_or_404(Profile, user__email=email_address)]
        except:
            profiles = Profile.objects.exclude(oauth_token__exact='').exclude(oauth_token_secret__exact='')
        try:
            limit = args[1]
        except:
            limit = 1000

        for profile in profiles:
            print "Getting mail for %s" % profile.user.email
            messages = profile.get_messages(limit)

            for gmessage in messages:
                message = messages.getMessage(gmessage.uid)

                try:
                    msg = Message.objects.get(
                        profile=profile,
                        m_uid=message.uid)
                except:
                    # Check To and From addresses for Contact
                    contact = self.get_contact(message.To, message.From, profile)

                    msg = Message()
                    msg.profile = profile
                    msg.m_uid = message.uid
                    msg.m_date = parse(message.date)
                    msg.m_from = self.parse_address(message.From)
                    msg.m_to = self.parse_address(message.To)
                    msg.m_subject = self.parse_subject(message.Subject)
                    msg.m_body = self.parse_body(message.Body)
                    msg.contact_id = contact.pk
                    if contact.client:
                        msg.client = contact.client
                    msg.save()
