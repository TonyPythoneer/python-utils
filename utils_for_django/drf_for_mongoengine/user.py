#!/usr/bin/env python
# -*- coding: utf-8 -*-
#  @first_date    20151016
#  @date          20151016
#  @version       0.0
"""Customize User object for mongoengine

.. _It's copied form:
    https://github.com/MongoEngine/mongoengine/blob/0.9/mongoengine/django/auth.py#L202
"""
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth.hashers import check_password, make_password

from mongoengine import fields, Document
from mongoengine.django.utils import datetime_now
from mongoengine.django.auth import MongoEngineBackend


class User(Document):
    """A User document that aims to mirror most of the API specified by Django
    at http://docs.djangoproject.com/en/dev/topics/auth/#users
    """
    # basic info fields
    username = fields.StringField(max_length=30, required=True)
    email = fields.EmailField()
    password = fields.StringField(max_length=128)
    displayname = fields.StringField(max_length=30)

    # permission info fields
    is_active = fields.BooleanField(default=True)
    is_superuser = fields.BooleanField(default=False)
    is_staff = fields.BooleanField(default=False)

    # datetime info fields
    changed_pwd_at = fields.DateTimeField()
    last_login = fields.DateTimeField(default=datetime_now)
    date_joined = fields.DateTimeField(default=datetime_now)

    # meta
    meta = {
        'allow_inheritance': True,
        'indexes': [
            {'fields': ['username'], 'unique': True, 'sparse': True}
        ]
    }

    def __unicode__(self):
        return self.username

    def is_anonymous(self):
        return False

    def is_authenticated(self):
        return True

    def is_admin(self):
        return self.is_active and self.is_superuser and self.is_staff

    def set_password(self, raw_password):
        """Sets the user's password - always use this rather than directly
        assigning to :attr:`~mongoengine.django.auth.User.password` as the
        password is hashed before storage.
        """
        now = datetime_now()
        self.password = make_password(raw_password)
        self.changed_pwd_at = now
        self.save()
        return self

    def check_password(self, raw_password):
        """Checks the user's password against a provided password - always use
        this rather than directly comparing to
        :attr:`~mongoengine.django.auth.User.password` as the password is
        hashed before storage.
        """
        return check_password(raw_password, self.password)

    @classmethod
    def create_user(cls, username, password, email=None):
        """Create (and save) a new user with the given username, password and
        email address.
        """
        now = datetime_now()

        # Normalize the address by lowercasing the domain part of the email
        # address.
        if email is not None:
            try:
                email_name, domain_part = email.strip().split('@', 1)
            except ValueError:
                pass
            else:
                email = '@'.join([email_name, domain_part.lower()])

        user = cls(username=username, email=email,
                   date_joined=now, changed_pwd_at=now)
        user.set_password(password)
        user.save()
        return user

    @classmethod
    def login(cls, username, password):
        """Create (and save) a new user with the given username, password and
        email address.
        """
        now = datetime_now()

        if username:
            user = cls.objects(username=username).first()
        else:
            return None

        if not user.check_password:
            return None

        user.last_login = now
        user.save()

        return user

    def email_user(self, subject, message, from_email=None):
        "Sends an e-mail to this User."
        from django.core.mail import send_mail
        send_mail(subject, message, from_email, [self.email])


def get_user(userid):
    """Returns a User object from an id (User.id). Django's equivalent takes
    request, but taking an id instead leaves it up to the developer to store
    the id in any way they want (session, signed cookie, etc.)
    """
    if not userid:
        return AnonymousUser()
    return MongoEngineBackend().get_user(userid) or AnonymousUser()
