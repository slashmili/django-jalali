from distutils.version import StrictVersion
import django
import sys

django_version = django.get_version()
if StrictVersion(django_version) >= StrictVersion('1.9'):
    from django.template import Library
else:
    from django.template.base import Library

register = Library()


@register.filter(expects_localtime=True, is_safe=False)
def jformat(value, arg=None):
    """Formats a date or time according to the given format."""
    if value in (None, ''):
        return ''
    if arg is None:
        arg = "%c"
    try:
        if StrictVersion(django_version) < StrictVersion('1.8'):
            if sys.version_info >= (3, ): # python 3
                arg = str(arg)
            else: # python2
                arg = arg.encode('utf-8')

        return value.strftime(arg)
    except AttributeError:
        return ''
