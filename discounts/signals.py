# discounts/signals.py

from django.db.models.signals import post_save
from django.dispatch import receiver

from discounts.models import Discount
from discounts.services import refresh_discount_prices


@receiver(post_save, sender=Discount)
def discount_saved(sender, instance, **kwargs):
    refresh_discount_prices(instance)