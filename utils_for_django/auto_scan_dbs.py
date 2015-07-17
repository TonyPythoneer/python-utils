#!/usr/bin/env python
# -*- coding: utf-8 -*-
#  @first_date    20150717
#  @date          20150717
#  @version       0.0
"""One method replace local_setting.py of method but the scan only happen one time.
So it can't get the newest db status when DB Admin add new db.
"""

import django
from django.conf import settings
config_db = settings.DATABASES[settings.CONFIG_DBNAME]
db = MySQLdb.connect(user=config_db["USER"],
                     passwd=config_db["PASSWORD"],
                     host=config_db["HOST"],
                     db=config_db["NAME"])
cursor = db.cursor()

query = ("SELECT * FROM %s" % ("DbList"))
cursor.execute(query)

for (index, p2pname, ip, port, dbname) in cursor:
    settings.DATABASES[dbname] = {
        'ENGINE': 'django.db.backends.mysql',
        'HOST': config_db["HOST"],
        'PORT': 3306,
        'NAME': dbname,
        'USER': config_db["USER"],
        'PASSWORD': config_db["PASSWORD"],
        'ENCODING': 'utf-8',
    }


reload(django)

cursor.close()
