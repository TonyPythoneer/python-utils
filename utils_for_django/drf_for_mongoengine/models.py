import binascii
import os

from django.conf import settings
from django.utils.timezone import now

from mongoengine import Document, StringField, ReferenceField, CASCADE
from mongoengine.fields import DateTimeField

AUTH_USER_MODEL = getattr(settings, 'AUTH_USER_MODEL', 'auth.user')


class MongoToken(Document):
    key = StringField(max_length=40)
    user = ReferenceField('PortalUser', required=True, reverse_delete_rule=CASCADE)
    created = DateTimeField()

    def __init__(self, *args, **values):
        super().__init__(*args, **values)
        if not self.key:
            self.key = self.generate_key()

    def save(self, *args, **kwargs):
        if not self.id:
            self.created = now()

        return super().save(*args, **kwargs)

    def generate_key(self):
        return binascii.hexlify(os.urandom(20)).decode()

    def __unicode__(self):
        return self.key
