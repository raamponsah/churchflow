from django.db import models


# Create your models here.
from django.db.models.signals import post_save
from django.dispatch import receiver

from membership.models import Member
from utilities.send_sms import send_sms


class Announcement(models.Model):
    title = models.CharField(max_length=255, null=False, blank=False)
    description = models.TextField(null=False, blank=False)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Announcement'
        verbose_name_plural = 'Announcement'

    def __str__(self):
        return self.title


@receiver(post_save, sender=Announcement)
def notify_members(sender, instance, created, **kwargs):
    if created:
        members = Member.objects.all()
        for member in members:
            send_sms(sendto=member.primary_phone, message_content=f"Announcement - {instance}"
                                           f"\n {instance.description}\n")