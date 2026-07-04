from addresses.models import Address
from addresses.services.address import set_default_address
from addresses.validators import validate_address_owner
from carts.selectors import get_user_active_cart

from addresses.selectors import (
    get_user_addresses,
    get_address_by_id, get_default_address,
)
from discounts.models import Coupon
from discounts.selectors import get_coupon_by_code

from discounts.services.coupon import validate_coupon
from shipping.selectors import get_shipping_method_by_id

from shipping.services.shipping_method import (
    get_available_shipping_methods
)

from orders.services import create_order_from_cart

from payments.services.payment import create_payment
from shipping.validators import validate_shipping_method_available


# =====================================================
# Checkout Preview
# =====================================================

# def preview_checkout(
#     *,
#     user,
# ):
#     """
#     دریافت اطلاعات اولیه Checkout.
#
#     شامل:
#         - سبد خرید
#         - آدرس‌های کاربر
#         - روش‌های ارسال هر آدرس
#     """
#
#     cart = get_user_active_cart(user)
#
#     addresses = get_user_addresses(user=user)
#
#     checkout_addresses = []
#
#     for address in addresses:
#         shipping_methods = get_available_shipping_methods(
#             cart=cart,
#             address=address,
#         )
#
#         checkout_addresses.append({
#             "address": address,
#             "shipping_methods": shipping_methods,
#         })
#
#     return {
#         "cart": cart,
#         "addresses": checkout_addresses,
#     }


# =====================================================
# Checkout Summary
# =====================================================

def prepare_checkout(
    *,
    user,
    address_id: int | None = None,
    shipping_method_id: int | None = None,
    coupon_code: str | None = None,
) -> dict:
    """
    محاسبه پیش‌نمایش Checkout.

    در این مرحله هیچ Order ساخته نمی‌شود.
    """

    cart = get_user_active_cart(user)

    addresses = get_user_addresses(user=user)
    if address_id is not None:
        address = get_address_by_id(
            address_id=address_id,
            addresses=addresses,
        )
        set_default_address(address=address)
    else:
        address = get_default_address(
            user=user,
            addresses=addresses
        )

    available_shipping_methods = get_available_shipping_methods(
        cart=cart,
        address=address,
    )

    if shipping_method_id is not None:
        shipping_method = get_shipping_method_by_id(shipping_method_id=shipping_method_id)
        validate_shipping_method_available(
            shipping_method=shipping_method,
            available_shipping_methods=available_shipping_methods,
        )

    else:
        shipping_method = available_shipping_methods.first()

    coupon = None

    if coupon_code is not None:
        coupon = get_coupon_by_code(code=coupon_code)
        coupon = validate_coupon(
            coupon=coupon,
            user=user
        )


    shipping_cost = shipping_method.price

    return {
        "cart": cart,
        "address": address,
        "shipping_method": shipping_method,
        "coupon": coupon,
        "shipping_cost": shipping_cost,
    }


# =====================================================
# Checkout Confirm
# =====================================================

def confirm_checkout(
    *,
    user,
    address_id,
    shipping_method_id,
    coupon: Coupon | None = None,
    gateway_type,
    callback_url,
    note="",
):
    """
    تایید Checkout.

    ایجاد Order و سپس Payment.
    """

    order = create_order_from_cart(
        user=user,
        address_id=address_id,
        shipping_method_id=shipping_method_id,
        coupon=coupon,
        note=note,
    )

    payment = create_payment(
        order=order,
        gateway_type=gateway_type,
        callback_url=callback_url
    )

    return payment