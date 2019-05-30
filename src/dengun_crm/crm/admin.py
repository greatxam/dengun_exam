# Created by Maximillian M. Estrada on 30-May-2019

from django.contrib import admin

from crm.models import *

class ContactAdmin(admin.ModelAdmin):
    list_display = [
        'last_name',
        'first_name',
        'middle_name',
        'email',
        'contact_number']
    search_fields = ['last_name', 'first_name']

class CampaignContactInline(admin.TabularInline):
    model = CampaignContact
    extra = 1
    raw_id_fields = ('contact',)
    readonly_fields = ('status',)

class CampaignAdmin(admin.ModelAdmin):
    inlines = [CampaignContactInline,]

    list_display = ['subject', 'created', 'modified']
    search_fields = ['subject']

admin.site.register(Contact, ContactAdmin)
admin.site.register(Campaign, CampaignAdmin)
