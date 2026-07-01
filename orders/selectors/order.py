from django.db.models import Prefetch

from orders.models import Order, OrderItem
from orders.constants import OrderStatus


def get_order_queryset():
    """
    Base queryset for all order selectors.
    """

    return (
        Order.objects
        .select_related(
            "user",
            "coupon",
        )
        .prefetch_related(
            Prefetch(
                "items",
                queryset=OrderItem.objects.select_related(
                    "product",
                    "variant",
                ),
            )
        )
    )


def get_order_by_id(order_id: int):
    """
    Get order by id.
    """

    return (
        get_order_queryset()
        .filter(id=order_id)
        .first()
    )


def get_order_by_number(order_number: str):
    """
    Get order by order_number.
    """

    return (
        get_order_queryset()
        .filter(order_number=order_number)
        .first()
    )


def get_user_orders(user):
    """
    All user orders.
    """

    return (
        get_order_queryset()
        .filter(user=user)
    )


def get_user_order_by_id(user, order_id: int):
    """
    Single user order.
    """

    return (
        get_order_queryset()
        .filter(
            user=user,
            id=order_id,
        )
        .first()
    )


def get_user_order_by_number(user, order_number: str):
    """
    Single user order by order number.
    """

    return (
        get_order_queryset()
        .filter(
            user=user,
            order_number=order_number,
        )
        .first()
    )


def get_user_pending_orders(user):
    """
    Pending orders.
    """

    return (
        get_order_queryset()
        .filter(
            user=user,
            status=OrderStatus.PENDING,
        )
    )


def get_user_confirmed_orders(user):
    """
    Confirmed orders.
    """

    return (
        get_order_queryset()
        .filter(
            user=user,
            status=OrderStatus.CONFIRMED,
        )
    )


def get_user_processing_orders(user):
    """
    Processing orders.
    """

    return (
        get_order_queryset()
        .filter(
            user=user,
            status=OrderStatus.PROCESSING,
        )
    )


def get_user_completed_orders(user):
    """
    Completed orders.
    """

    return (
        get_order_queryset()
        .filter(
            user=user,
            status=OrderStatus.COMPLETED,
        )
    )


def get_user_canceled_orders(user):
    """
    Canceled orders.
    """

    return (
        get_order_queryset()
        .filter(
            user=user,
            status=OrderStatus.CANCELED,
        )
    )


def get_orders_by_status(status: str):
    """
    Admin selector.
    """

    return (
        get_order_queryset()
        .filter(status=status)
    )


def get_recent_orders(limit: int = 10):
    """
    Recent orders.
    """

    return (
        get_order_queryset()
        .order_by("-created_at")[:limit]
    )


def get_order_items(order):
    """
    Order items.
    """

    return (
        order.items
        .select_related(
            "product",
            "variant",
        )
        .all()
    )


from django.db.models import Count, Sum
from django.utils import timezone


def get_orders_created_today():
    """
    سفارش‌های امروز
    Orders created today.
    """

    today = timezone.localdate()

    return (
        get_order_queryset()
        .filter(created_at__date=today)
    )


def get_orders_created_between(
    *,
    start_date,
    end_date,
):
    """
    سفارش‌های بازه زمانی
    Orders created between two dates.
    """

    return (
        get_order_queryset()
        .filter(
            created_at__date__gte=start_date,
            created_at__date__lte=end_date,
        )
    )


def get_user_orders_count(user):
    """
    تعداد سفارش‌های یک کاربر
    Total user orders count.
    """

    return (
        Order.objects
        .filter(user=user)
        .count()
    )


def get_orders_count_by_status(status: str):
    """
    تعداد سفارش‌ها بر اساس وضعیت
    Orders count by status.
    """

    return (
        Order.objects
        .filter(status=status)
        .count()
    )


def get_total_sales_amount():
    """
    مبلغ کل فروش
    Total sales amount.
    """

    return (
        Order.objects.aggregate(
            total=Sum("total_amount")
        )["total"]
        or 0
    )


def get_total_completed_sales_amount():
    """
    مبلغ فروش سفارش‌های تکمیل شده
    Completed sales amount.
    """

    return (
        Order.objects.filter(
            status=OrderStatus.COMPLETED
        )
        .aggregate(
            total=Sum("total_amount")
        )["total"]
        or 0
    )


def get_sales_amount_between(
    *,
    start_date,
    end_date,
):
    """
    مبلغ فروش بازه زمانی
    Sales amount between dates.
    """

    return (
        Order.objects.filter(
            created_at__date__gte=start_date,
            created_at__date__lte=end_date,
        )
        .aggregate(
            total=Sum("total_amount")
        )["total"]
        or 0
    )


def get_average_order_value():
    """
    میانگین ارزش سفارش (AOV)
    Average order value.
    """

    orders = Order.objects.count()

    if not orders:
        return 0

    total_sales = get_total_sales_amount()

    return total_sales / orders


def get_top_customers(limit=10):
    """
    پرفروش‌ترین کاربران
    Top customers by sales amount.
    """

    return (
        Order.objects
        .values(
            "user_id",
            "user__first_name",
            "user__last_name",
            "user__phone_number",
        )
        .annotate(
            orders_count=Count("id"),
            total_spent=Sum("total_amount"),
        )
        .order_by("-total_spent")[:limit]
    )


def get_top_selling_products(limit=10):
    """
    پرفروش‌ترین محصولات
    Top selling products.
    """

    return (
        OrderItem.objects
        .values(
            "product_id",
            "product__name",
        )
        .annotate(
            total_quantity=Sum("quantity"),
        )
        .order_by("-total_quantity")[:limit]
    )


def get_today_sales_amount():
    """
    درآمد امروز
    Today's sales amount.
    """

    today = timezone.localdate()

    return (
        Order.objects.filter(
            created_at__date=today
        )
        .aggregate(
            total=Sum("total_amount")
        )["total"]
        or 0
    )


def get_orders_dashboard_stats():
    """
    داشبورد مدیریتی (پیشنهاد حرفه‌ای)
    """
    return {
        "total_orders": Order.objects.count(),
        "pending_orders": get_orders_count_by_status(
            OrderStatus.PENDING
        ),
        "completed_orders": get_orders_count_by_status(
            OrderStatus.COMPLETED
        ),
        "today_orders": get_orders_created_today().count(),
        "today_sales": get_today_sales_amount(),
        "total_sales": get_total_sales_amount(),
    }