from django.db import transaction

from addresses.selectors import (
    get_address_by_id,
)
from carts.constants import CartStatus

from carts.selectors import (
    get_user_active_cart,
)

from carts.services.pricing import (
    calculate_cart_totals,
)

from orders.models import (
    Order,
    OrderItem,
)

from .validators import (
    validate_cart_exists,
    validate_cart_not_empty,
    validate_cart_status,
    validate_cart_stock,
    validate_address_owner, validate_address_exists,
)

from .snapshot import (
    build_address_snapshot,
    build_product_snapshot,
    build_shipping_snapshot
)

from .order_number import (
    generate_order_number,
)

from shipping.selectors import (
    get_shipping_method_by_id,
)

from shipping.validators import (
    validate_shipping_method_exists,
    validate_shipping_method_active,
)


@transaction.atomic
def create_order_from_cart(
    *,
    user,
    address_id,
    shipping_method_id,
    note="",
):
    cart = get_user_active_cart(user)
    note = note

    validate_cart_exists(cart)
    validate_cart_status(cart)
    validate_cart_not_empty(cart)
    validate_cart_stock(cart)

    address = get_address_by_id(
        address_id=address_id,
    )

    validate_address_exists(address)

    validate_address_owner(
        address,
        user,
    )

    shipping_method = (
        get_shipping_method_by_id(
            shipping_method_id,
        )
    )

    validate_shipping_method_exists(
        shipping_method,
    )

    validate_shipping_method_active(
        shipping_method,
    )


    totals = calculate_cart_totals(cart=cart)

    order = Order.objects.create(
        user=user,
        order_number=generate_order_number(),
        note=note,

        address_snapshot=build_address_snapshot(
            address
        ),

        subtotal=totals["subtotal"],
        discount_amount=totals["discount"],
        shipping_method=shipping_method,
        shipping_method_snapshot=
        build_shipping_snapshot(
            shipping_method
        ),
        shipping_cost=shipping_method.price,
        total_amount=(
                totals["total"]
                + shipping_method.price
        ),
    )

    order_items = []

    for cart_item in (
        cart.items
        .select_related(
            "variant__product",
            "variant",
        )
    ):
        variant = cart_item.variant

        order_items.append(
            OrderItem(
                order=order,

                product=cart_item.variant.product,
                variant=variant,

                quantity=cart_item.quantity,

                price=variant.price,

                discount_amount=0,

                final_price=variant.price,

                product_snapshot=build_product_snapshot(
                    product=cart_item.variant.product,
                    variant=variant,
                ),
            )
        )

        variant.stock -= cart_item.quantity
        variant.save(
            update_fields=["stock"]
        )

    OrderItem.objects.bulk_create(
        order_items
    )

    cart.status = CartStatus.CONVERTED
    cart.save(
        update_fields=["status"]
    )

    return order