from distutils.core import setup

setup(
        name='django_jalali',
        version='0.9',
        packages=['django_jalali',],
        description = ("Jalali Date support for Django model and admin interface"),
        url = 'http://github.com/slashmili/django-jalali',
        download_url = 'http://github.com/slashmili/django-jalali/tarball/master',
        author = 'Milad Rastian',
        author_email = 'eslashmili _at_ gmail.com',
        keywords = "django jalali",
        license='Python Software Foundation License',
        platforms='any',
        requires = ["jdatetime","django"],
        long_description=open('README').read()
)
