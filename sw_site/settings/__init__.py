"""
This is a django-split-settings main file.
For more information read this:
https://github.com/sobolevn/django-split-settings
Default environment is `developement`.
To change settings file:
`DJANGO_ENV=production python manage.py runserver`
"""

from split_settings.tools import optional, include
from os import environ
import os

ENV = environ.get('DJANGO_ENV') or 'development'

base_settings = [
    os.path.join('components','common.py'),
    os.path.join('environments','{}.py'.format(ENV)),
]

include(*base_settings)
