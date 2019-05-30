# Created by Maximillian M. Estrada on 30-May-2019

import uuid
from django.db import models

from crm.tasks import async_campaign_post_save

class Contact(models.Model):
    class Meta:
        db_table = 'crm_contacts'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100, null=True, blank=True)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    contact_number = models.CharField(max_length=20, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return  "{}, {} ({})".format(self.first_name, self.last_name, self.email)

class Campaign(models.Model):
    class Meta:
        db_table = 'crm_campaigns'
        ordering = ['-created']

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    subject = models.CharField(max_length=100)
    message = models.TextField()
    contacts = models.ManyToManyField('Contact', through='CampaignContact')
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{}".format(self.subject)

    def save(self):
        super().save()
        async_campaign_post_save.delay(self.pk)

        """
        for i in self.campaigncontact_set.all():
            if i.status == CampaignContact.PENDING:
                # celery task
                async_send_campaign_email.delay(i.campaign.pk, i.contact.pk)
        """

class CampaignContact(models.Model):
    PENDING,    SENT,   FAILED, = \
    0,          1,      2
    STATUS = (
        (PENDING, "Pending"),
        (SENT, "Sent"),
        (FAILED, "Failed")
    )

    class Meta:
        db_table = 'crm_campaigns_contacts'
        unique_together = (('campaign', 'contact'))

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE)
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE)
    status = models.PositiveSmallIntegerField(default=PENDING, choices=STATUS)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
