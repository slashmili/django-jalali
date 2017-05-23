from setuptools import setup, find_packages

setup(
        name='django-jalali',
        version='2.4.4',
        packages=find_packages(),
        include_package_data=True,
        zip_safe=False,
        description = ("Jalali Date support for Django model and admin interface"),
        url = 'http://github.com/slashmili/django-jalali',
        download_url = 'http://github.com/slashmili/django-jalali/tarball/master',
        author = 'Milad Rastian',
        author_email = 'eslashmili _at_ gmail.com',
        keywords = "django jalali",
        license='Python Software Foundation License',
        platforms='any',
        install_requires = ["jdatetime>=1.5","django>=1.7"],
        long_description=open('README.rst').read()
)
