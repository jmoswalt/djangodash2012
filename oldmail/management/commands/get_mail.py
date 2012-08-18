from django.core.management.base import BaseCommand, CommandError
from django.shortcuts import get_object_or_404

from oldmail.models import Profile, Message

class Command(BaseCommand):
    """
    Get mail for a Profile

    Needs 1 arg, the email address for the associated profile
    """

    def handle(self, *args, **options):
        email_address = args[0]
        try:
            limit = args[1]
        except:
            limit = 10

        profile = get_object_or_404(Profile, user__email=email_address)

        messages = profile.get_messages(limit)

        for msg in messages:
            message = messages.getMessage(msg.uid)
            print message
