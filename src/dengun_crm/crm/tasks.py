# Created by Maximillian M. Estrada on 30-May-2019

from __future__ import absolute_import, unicode_literals
import json
from celery import shared_task

from django.conf import settings
from django.core.mail import EmailMultiAlternatives, EmailMessage
from django.template.loader import get_template

@shared_task
def async_send_campaign_email(json_campaign, json_contact):
    campaign = json.loads(json_campaign)
    contact = json.loads(json_contact)
    context = {
        'campaign': campaign[0],
        'contact':contact[0]}
    print("<Celery Task: {subject}, {email}>".format(
        subject=campaign[0]['fields']['subject'],
        email=contact[0]['fields']['email']))

    # email content
    text_email = get_template('crm/campaign_email.txt')
    html_email = get_template('crm/campaign_email.html')

    email = EmailMultiAlternatives(
        campaign[0]['fields']['subject'],
        text_email.render(context),
        settings.ADMIN_EMAIL,
        [contact[0]['fields']['email']],
        reply_to=[settings.ADMIN_EMAIL])
    email.attach_alternative(html_email.render(context), "text/html")
    email.send()
