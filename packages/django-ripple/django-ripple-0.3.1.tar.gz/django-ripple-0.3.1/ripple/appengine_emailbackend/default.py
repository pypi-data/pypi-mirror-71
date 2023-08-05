import logging

from django.core.mail.backends.base import BaseEmailBackend
from django.core.mail import EmailMultiAlternatives
from django.core.exceptions import ImproperlyConfigured


try:
    from google.appengine.api import mail as aeemail
    from google.appengine.ext import deferred
except ImportError as err:
    raise ImproperlyConfigured(('Failed to import App Engine libraries: %s'
                                % err))


class EmailBackend(BaseEmailBackend):

    can_defer = False

    def send_messages(self, email_messages):
        num_sent = 0
        for message in email_messages:
            if self._send(message):
                num_sent += 1
        return num_sent

    def _copy_message(self, message):
        """Create and return App Engine EmailMessage class from message."""
        gmsg = aeemail.EmailMessage(sender=message.from_email,
                                    to=message.to,
                                    subject=message.subject,
                                    body=message.body)
        if message.extra_headers.get('Reply-To', None):
            gmsg.reply_to = message.extra_headers['Reply-To']
        if message.bcc:
            gmsg.bcc = list(message.bcc)
        if message.attachments:
            gmsg.attachments = [(a[0], a[1]) for a in message.attachments]
        if isinstance(message, EmailMultiAlternatives):  # look for HTML
            for content, mimetype in message.alternatives:
                if mimetype == 'text/html':
                    gmsg.html = content
                    break
        return gmsg

    def _send(self, message):
        try:
            msg = self._copy_message(message)
        except (ValueError, aeemail.InvalidEmailError) as err2:
            logging.warning(err2)
            if not self.fail_silently:
                raise
            return False
        if self.can_defer:
            deferred.defer(self._send_deferred, msg)
            return True
        try:
            msg.send()
        except aeemail.Error:
            if not self.fail_silently:
                raise
            return False
        return True

    def _send_deferred(self, msg):
        msg.send()
