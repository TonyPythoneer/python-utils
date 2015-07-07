#!/usr/bin/env python
# -*- coding: utf-8 -*-
#  @first_date    20150701
#  @date          20150701
'''
Sending mail cause program execution to be slow is main reason.
It's why it need to be separated from controller.

requirement:
Flask-Mail==0.9.0
'''
import os
from threading import Thread

from flask import Flask, render_template
from flask.ext.mail import Mail, Message

from manage import app

mail = Mail(app)


tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
the_app = Flask(__name__, template_folder=tmpl_dir)
mail = Mail(app)


def send_email(to, subject, template, **kwargs):
    msg = Message(app.config['FLASKY_MAIL_SUBJECT_PREFIX'] + subject,
                  sender=app.config['FLASKY_MAIL_SENDER'], recipients=[to])
    with the_app.app_context():
        msg.body = render_template(template + '.txt', **kwargs)
        msg.html = render_template(template + '.html', **kwargs)
        thr = Thread(target=send_async_email, args=[app, msg])
        thr.start()
        return thr


def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)
