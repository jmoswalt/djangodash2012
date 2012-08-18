from django.utils.functional import lazy
from django.core.urlresolvers import reverse


def lazy_reverse(name=None, *args):
    return lazy(reverse, str)(name, args=args)
