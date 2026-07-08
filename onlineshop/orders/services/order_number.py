from django.utils import timezone

from orders.models import Order


def generate_order_number():
    today = timezone.localdate()

    date_part = today.strftime("%Y%m%d")

    last_order = (
        Order.objects
        .order_by("-id")
        .only("id")
        .first()
    )

    sequence = 1

    if last_order:
        sequence = last_order.id + 1

    return (
        f"ORD-{date_part}-{sequence:06d}"
    )