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