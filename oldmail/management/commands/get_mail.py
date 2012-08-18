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
    def get_client(self, to_email_addr, from_email_addr, profile_email):
        c = None
        # First we check if the to address is the client.
        to_email = re.sub("(.*)<([\\w\\.\\@]+)>", "\\2", to_email_addr).split(',')[0]
        to_name = ''
        if "<" in to_email_addr:
            to_name = to_email_addr.split("<")[0].rstrip().replace("'", '').replace('"', '')
        # make sure the address is not the sender
        if to_email != profile_email:
            try:
                c = Contact.objects.get(email=to_email, name=to_name)
                return c
            except:
                c = Contact.objects.create(email=to_email, name=to_name)
                return c

        # now we check the from
        from_email = re.sub("(.*)<([\\w\\.\\@]+)>", "\\2", from_email_addr).split(',')[0]
        from_name = ''
        if "<" in from_email_addr:
            from_name = from_email_addr.split("<")[0].rstrip().replace("'", '').replace('"', '')
        if from_email != profile_email:
            try:
                c = Contact.objects.get(email=from_email, name=from_name)
                return c
            except:
                c = Contact.objects.create(email=from_email, name=from_name)
                return c

        # to email and from email are same as profile_email
        if to_email == from_email:
            c = Contact.objects.create(email=from_email)
            return c

    def parse_address(self, address):
        result = re.sub("(.*)<([\\w\\.\\@]+)>", "\\2", address)
        return result.split(',')[0]

    def handle(self, *args, **options):
        email_address = args[0]
        try:
            limit = args[1]
        except:
            limit = 10

        profile = get_object_or_404(Profile, user__email=email_address)

        messages = profile.get_messages(limit)

        for gmessage in messages:
            message = messages.getMessage(gmessage.uid)

            # Check To and From addresses for Contact
            contact = self.get_client(message.To, message.From, email_address)
            print contact.pk
            # Check Contact for number of Clients

            print self.parse_address(message.To)
            print "DATE: ", message.date

            try:
                msg = Message.objects.get(
                    profile=profile,
                    m_uid=message.uid)
            except:
                msg = Message()
                msg.profile = profile
                msg.m_uid = message.uid
                msg.m_date = parse(message.date)
                msg.m_from = self.parse_address(message.From)
                msg.m_to = self.parse_address(message.To)
                msg.m_subject = message.Subject
                msg.m_body = message.Body
                msg.contact_id = contact.pk
                msg.save()
