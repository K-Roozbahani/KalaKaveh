from django.db import models

from .constants import PaymentStatus


class PaymentManager(models.Manager):

    def pending(self):
        return self.filter(
            status=PaymentStatus.PENDING,
        )

    def successful(self):
        return self.filter(
            status=PaymentStatus.SUCCESS,
        )

    def failed(self):
        return self.filter(
            status=PaymentStatus.FAILED,
        )

    def canceled(self):
        return self.filter(
            status=PaymentStatus.CANCELED,
        )

    def refunded(self):
        return self.filter(
            status=PaymentStatus.REFUNDED,
        )