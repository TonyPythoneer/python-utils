#!/usr/bin/env python
# -*- coding: utf-8 -*-
#  @first_date    20150825
#  @date          20150825 - Build db_setting
#  @version       0.0
"""DB Settings
"""
import sys, os

try:
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),
                    '../../website')))

    from website import settings
    DATABASES = settings.DATABASES
except:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'HOST': '',
            'PORT': 3306,
            'NAME': 'dbname',
            'USER': 'root',
            'PASSWORD': 'root',
            'ENCODING': 'utf-8',
        },
    }


# Define db configure of sqlalchemy
DB_CONF = {
    'driver': 'mysql',
    'host': DATABASES['default']['HOST'],
    'user': DATABASES['default']['USER'],
    'password': DATABASES['default']['PASSWORD'],
    'db': DATABASES['default']['NAME'],
    'encoding': DATABASES['default']['ENCODING'],
    'tables': {'Health': 'Health'},
}
