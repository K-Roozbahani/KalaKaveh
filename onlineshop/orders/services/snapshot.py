def build_address_snapshot(address):
    return {
        "receiver_name": address.receiver_name,
        "receiver_phone": str(address.receiver_phone),

        "province": address.province.name,
        "city": address.city.name,

        "address_line": address.address_line,

        "plaque": address.plaque,
        "unit": address.unit,

        "postal_code": address.postal_code,

        "latitude": address.latitude,
        "longitude": address.longitude,
    }


def build_product_snapshot(
    *,
    product,
    variant,
):
    image = product.images.first()

    return {
        "product_id": product.id,
        "product_name": product.name,
        "product_image": image.image.url if image else None,

        "variant_id": variant.id,
        "variant_name": str(variant),
        "sku": variant.sku,
    }


def build_shipping_snapshot(
    shipping_method,
):
    return {
        "id": shipping_method.id,
        "name": shipping_method.name,
        "price": str(
            shipping_method.price
        ),
        "estimated_days": (
            shipping_method.estimated_days
        ),
    }