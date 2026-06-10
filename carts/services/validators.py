from rest_framework.exceptions import ValidationError


def validate_variant_availability(*, variant, quantity):
    """
    بررسی موجودی کالا.
    """

    if quantity > variant.stock:
        raise ValidationError(
            {
                "quantity": "تعداد درخواستی بیشتر از موجودی کالا است."
            }
        )