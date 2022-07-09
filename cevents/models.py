from django.db import models

# Create your models here.
from django.db.models.signals import post_save
from django.dispatch import receiver

from membership.models import Member
from utilities.send_sms import send_sms


class ChurchEvent(models.Model):
    types = (
        ('one-time', 'One-Time'),
        ('recurring', 'Recurring'),
    )
    title = models.CharField(max_length=255, null=False, blank=False)
    description = models.TextField(max_length=255, null=False, blank=False)
    start_date = models.DateTimeField(max_length=255, null=False, blank=False)
    end_date = models.DateTimeField(max_length=255, null=False, blank=False)
    venue = models.CharField(max_length=255, null=False, blank=False)
    type = models.CharField(max_length=20, choices=types, default=None)
    notify_members = models.BooleanField(default=False)

    def __str__(self):
        return self.title


@receiver(post_save, sender=ChurchEvent)
def notify_members(sender, instance, created, **kwargs):
    if created:
        members = Member.objects.all()
        for member in members:
            send_sms(sendto=member.primary_phone, message_content=f"Upcoming Event - {instance}"
                                           f"\n Start Date: {instance.start_date}\n End Date: {instance.end_date}\n"
                                           f"{instance.venue}\n You are warmly invited. See you soon.")