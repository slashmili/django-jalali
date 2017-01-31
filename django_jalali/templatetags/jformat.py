from distutils.version import StrictVersion
import django

if StrictVersion(django.get_version()) >= StrictVersion('1.9'):
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
        return value.strftime(arg)
    except AttributeError:
        return ''
