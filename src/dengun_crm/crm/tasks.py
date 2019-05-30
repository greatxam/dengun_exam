# Created by Maximillian M. Estrada on 30-May-2019

from __future__ import absolute_import, unicode_literals
from celery import shared_task

from django.conf import settings
from django.core.mail import EmailMultiAlternatives, EmailMessage
from django.template.loader import get_template

from crm import models as crm_models

@shared_task
def async_campaign_post_save(campaign_pk):
    campaign = crm_models.Campaign.objects.get(pk=campaign_pk)

    for i in campaign.campaigncontact_set.all():
        # don't process SENT status
        if i.status == crm_models.CampaignContact.SENT:
            continue
        async_send_campaign_email(i)

def async_send_campaign_email(campaign_contact):
    campaign = campaign_contact.campaign
    contact = campaign_contact.contact
    context = {
        'campaign': campaign,
        'contact':contact}
    print("<Celery Task: {subject}, {email}>".format(
        subject=campaign.subject,
        email=contact.email))

    # email content
    text_email = get_template('crm/campaign_email.txt')
    html_email = get_template('crm/campaign_email.html')

    email = EmailMultiAlternatives(
        campaign.subject,
        text_email.render(context),
        settings.ADMIN_EMAIL,
        [contact.email],
        reply_to=[settings.ADMIN_EMAIL])
    email.attach_alternative(html_email.render(context), "text/html")
    try:
        email.send()
        campaign_contact.status = crm_models.CampaignContact.SENT
    except:
        campaign_contact.status = crm_models.CampaignContact.FAILED
    campaign_contact.save()
