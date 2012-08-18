import random
import string

from django.utils.functional import lazy
from django.core.urlresolvers import reverse
from django.conf import settings
from django.core.mail.message import EmailMessage
from django.core.mail import get_connection


def random_string(n=50):
    return ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for x in range(n))


def lazy_reverse(name=None, *args):
    return lazy(reverse, str)(name, args=args)


def send_email(subject, message, recipient_list, fail_silently=False):
    conn = get_connection(fail_silently=fail_silently)

    msg = EmailMessage(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            recipient_list,
            connection=conn
            )

    msg.content_subtype = "html"

    msg.send()

    return True
