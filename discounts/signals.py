# discounts/signals.py

from django.db.models.signals import post_save, post_delete

from django.dispatch import receiver

from discounts.models import Discount
from discounts.services import refresh_discount_prices


@receiver(post_save, sender=Discount)
def discount_saved(sender, instance, **kwargs):
    refresh_discount_prices(instance)

@receiver(post_delete, sender=Discount)
def discount_deleted(sender, instance, **kwargs):
    refresh_discount_prices(instance)