from django.db import transaction

from addresses.selectors import (
    get_address_by_id,
)

from carts.selectors import (
    get_user_active_cart,
)

from carts.services.totals import (
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
    validate_address_owner,
)

from .snapshot import (
    build_address_snapshot,
    build_product_snapshot,
)

from .order_number import (
    generate_order_number,
)


@transaction.atomic
def create_order_from_cart(
    *,
    user,
    address_id,
):
    cart = get_user_active_cart(user)

    validate_cart_exists(cart)
    validate_cart_status(cart)
    validate_cart_not_empty(cart)
    validate_cart_stock(cart)

    address = get_address_by_id(address_id)

    validate_address_owner(
        address,
        user,
    )

    totals = calculate_cart_totals(cart)

    order = Order.objects.create(
        user=user,
        order_number=generate_order_number(),

        address_snapshot=build_address_snapshot(
            address
        ),

        subtotal=totals["subtotal"],
        discount_amount=totals["discount_amount"],
        shipping_cost=totals.get(
            "shipping_cost",
            0,
        ),
        total_amount=totals["total"],
    )

    order_items = []

    for cart_item in (
        cart.items
        .select_related(
            "product",
            "variant",
        )
    ):
        variant = cart_item.variant

        order_items.append(
            OrderItem(
                order=order,

                product=cart_item.product,
                variant=variant,

                quantity=cart_item.quantity,

                price=variant.price,

                discount_amount=0,

                final_price=variant.price,

                product_snapshot=build_product_snapshot(
                    product=cart_item.product,
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

    cart.status = cart.Status.CONVERTED
    cart.save(
        update_fields=["status"]
    )

    return order