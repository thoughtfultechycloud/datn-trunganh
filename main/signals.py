from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import AccountCategory, AccountOpeningBalance


@receiver(post_save, sender=AccountCategory)
def create_opening_balance(sender, instance, created, **kwargs):
    if created:
        AccountOpeningBalance.objects.get_or_create(account=instance)
