from django.utils.translation import gettext_lazy as _


class CartStatus:

    ACTIVE = "active"
    CONVERTED = "converted"
    ABANDONED = "abandoned"

    CHOICES = (
        (ACTIVE,  _("فعال")),
        (CONVERTED, _("تبدیل شده به سفارش")),
        (ABANDONED, _("رها شده")),
    )