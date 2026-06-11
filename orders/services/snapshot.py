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
    return {
        "product_id": product.id,
        "product_name": product.name,

        "variant_id": variant.id,
        "variant_name": str(variant),

        "sku": variant.sku,
    }