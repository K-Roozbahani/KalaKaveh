from django.db import models

from .constants import OrderStatus


class OrderQuerySet(models.QuerySet):

    def pending(self):
        return self.filter(status=OrderStatus.PENDING)

    def confirmed(self):
        return self.filter(status=OrderStatus.CONFIRMED)

    def completed(self):
        return self.filter(status=OrderStatus.COMPLETED)


class OrderManager(models.Manager):

    def get_queryset(self):
        return OrderQuerySet(self.model, using=self._db)

    def pending(self):
        return self.get_queryset().pending()

    def confirmed(self):
        return self.get_queryset().confirmed()

    def completed(self):
        return self.get_queryset().completed()