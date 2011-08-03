from setuptools import setup, find_packages

setup(
        name='django_jalali',
        version='0.9',
        packages=find_packages(),
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
