#!/usr/bin/env python
# -*- coding: utf-8 -*-
#  @first_date    20150702
#  @date          20150702
#  @version       0.0
'''
Create Multipurpose Internet Mail Extensions (MIME) Mail
'''
import smtplib

from datetime import datetime

from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.encoders import encode_base64


# Recommand: It can set in setting when you develop in django.
MAIL_CONF = {
    'host': 'mail.server.com',
    'port': 25,
    'sender': 'admin@example.com',

    '_signup': {
        'sender_title': 'Welcome to website',
        'user_title': 'Dear user',
        'subject': 'Your account is created',
        'text': 'Welcome!',
    },
    '_reset_pwd': {
        'sender_title': 'forget pwd email',
        'user_title': 'Dear user',
        'subject': 'Do you ferget pwd?',
        'text': 'Please click here and change your password',
    },
}


def __read_file(file_object):
    '''Read file

    Args:
        file_object (Obj): File

    Return:
        (String) file content
    '''

    while True:
        # f.read(size) reads some quantity of data and returns it as a string.
        # size is an optional numeric argument.
        f_data = file_object.read(64 * 1024)  # Read 64 KB

        if not f_data:
            break
        yield f_data


def CreateMimeMail(mailto, fromwho, subject, maintxt, attachs):
    '''
    CreateMimeMail() is a function to help create MIME message with attachment
    easily.

    Args:
        mailto (String): who are the reciptients
        fromwho (String): who send this mail
        subject (String): mail of subject
        maintxt (String): mail of main body text.
        attachs (List-Obj): The attached file list

    Return:
        (Obj) a MIME message
    '''
    msg = MIMEMultipart()
    msg['To'], msg['From'], msg['Subject'] = mailto, fromwho, subject
    msg.preamble = "If you see this, your MTA doesn't support MIME."
    msg.attach(MIMEText(maintxt, _charset='utf-8'))
    # HTML content
    # msg.attach(MIMEText(maintxt, "html", _charset='utf-8'))

    # Email: attachment
    for f_obj in attachs:
        attach = MIMEBase('application', 'octet-stream')

        f_data = ''.join(__read_file(f_obj))
        filename = '{}.jpg'.format(datetime.now().strftime("%Y-%m-%d-%H:%M:%S"))

        # Set the entire message object’s payload to payload.
        # It is the client’s responsibility to ensure the payload invariants.
        attach.set_payload(f_data)

        encode_base64(attach)
        attach.add_header('Content-Disposition', 'attachment', filename=filename)
        msg.attach(attach)
    return msg


class Poster:
    '''
    email poster
    '''

    def __init__(self, **email_inf):
        '''
        Base mail settings

        Args:
            (Dict) email settings
        '''

        mail_conf = MAIL_CONF

        self.host_server = mail_conf.get('host')
        self.host_server_port = mail_conf.get('port', 25)
        self.sender = mail_conf.get('sender', 'admin@example.com')

        self.to_email = email_inf.get('to_email', 'admin@example.com')
        self.user_account = email_inf.get('account', self.to_email)
        mail_type = email_inf.get('mail_type')

        text_msg = []
        if mail_type == 0:  # register / re-send active code
            mail_content = mail_conf['_signup']

            self.sender_name = mail_content.get('sender_title')
            self.user_name = mail_content.get('user_title')
            self.subject = mail_content.get('subject')

            text_msg = [
                mail_content.get('text'),
                # email_inf.get('active_code', 'TEST'),
            ]
        elif mail_type == 1:  # forgot password (changed confirm code)
            mail_content = mail_conf['_reset_pwd']

            self.sender_name = mail_content.get('sender_title')
            self.user_name = mail_content.get('user_title')
            self.subject = mail_content.get('subject')

            text_msg = [
                mail_content.get('text'),
                email_inf.get('reset_pwd_code', 'default'),
            ]

        self.mail_text = '\n'.join(text_msg)

    def send_mail(self, attach_files=None):
        '''Send mail

        Args:
            attach_files (List): attach files

        Return:
            (Boolean) Success or Fail
        '''
        if attach_files is None:
            attach_files = []

        msg = CreateMimeMail(self.to_email, self.sender, self.subject,
                             self.mail_text, attach_files)
        try:
            service = smtplib.SMTP(self.host_server, self.host_server_port)
            repo = service.sendmail(msg['From'], msg['To'], msg.as_string())
        except smtplib.SMTPException:
            return False

        if repo:
            return False
        service.quit()

        return True
