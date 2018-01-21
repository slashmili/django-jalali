#!/bin/bash -xe
PYTHON_VER=$(python -c 'import sys; print(".".join(map(str, sys.version_info[:1])))')
if [[ "$PYTHON_VER" = "2" && "$DJANGO" = "2.0" ]]; then
    echo "Django 2.0 only supports Python 3 and above"
    exit 0;
fi
cd jalali_test
python manage.py test
cd ..
python setup.py sdist
pip install dist/django-jalali*
