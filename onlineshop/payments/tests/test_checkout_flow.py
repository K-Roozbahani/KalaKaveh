from django.test import TestCase
from unittest.mock import patch

from payments.services.callback import process_gateway_callback
from users.models import User

from addresses.models import (
    Province,
    City,
    Address,
)

from products.models import (
    Product,
    ProductVariant,
)

from carts.models import (
    Cart,
    CartItem,
)

from carts.constants import CartStatus

from orders.models import Order

from orders.services.order import (
    create_order_from_cart,
)

from payments.services.payment import (
    create_payment,
)

from payments.services.payment import (
    verify_payment,
)

from payments.constants import GatewayType

from shipping.models import Shipment

from shipping.tests.factories import (
    create_shipping_method,
)


class CheckoutFlowTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            phone_number="09120000000",
            password="test123",
        )

        self.province = Province.objects.create(
            name="تهران",
        )

        self.city = City.objects.create(
            province=self.province,
            name="تهران",
        )

        self.address = Address.objects.create(
            user=self.user,
            title="خانه",
            receiver_name="علی رضایی",
            receiver_phone="09120000000",
            province=self.province,
            city=self.city,
            address_line="خیابان تست",
            postal_code="1234567890",
        )

        self.product = Product.objects.create(
            name="محصول تست",
            slug="test-product",
        )

        self.variant = ProductVariant.objects.create(
            product=self.product,
            sku="SKU-001",
            price=100000,
            stock=10,
        )

        self.cart = Cart.objects.create(
            user=self.user,
            status=CartStatus.ACTIVE,
        )

        CartItem.objects.create(
            cart=self.cart,
            variant=self.variant,
            quantity=2,
        )

        self.shipping_method = create_shipping_method()

    @patch(
        "payments.services.gateways.get_gateway"
    )
    def test_checkout_flow(
        self,
        mock_gateway,
    ):
        """
        Cart → Order → Payment → Shipment (FULL FLOW)
        """

        # ----------------------------
        # Gateway Mock
        # ----------------------------
        mock_gateway.return_value.verify_payment.return_value = {
            "success": True,
            "ref_id": "REF123",
        }

        # ----------------------------
        # Order
        # ----------------------------
        order = create_order_from_cart(
            user=self.user,
            address_id=self.address.id,
            shipping_method_id=self.shipping_method.id,
        )

        self.assertEqual(
            Order.objects.count(),
            1,
        )

        self.assertEqual(
            order.shipping_method,
            self.shipping_method,
        )

        # ----------------------------
        # Payment
        # ----------------------------
        result = create_payment(
            order=order,
            gateway_type=GatewayType.ZARINPAL,
            callback_url="https://example.com/callback",
        )

        payment = result["payment"]

        process_gateway_callback(
            authority=payment.authority,
        )

        payment.refresh_from_db()
        order.refresh_from_db()

        # ----------------------------
        # Payment Assertions
        # ----------------------------
        self.assertIsNotNone(
            payment.paid_at,
        )

        self.assertIsNotNone(
            order.paid_at,
        )

        self.assertEqual(
            payment.status,
            "success",
        )

        # ----------------------------
        # Shipment
        # ----------------------------
        self.assertEqual(
            Shipment.objects.count(),
            1,
        )

        shipment = Shipment.objects.get(
            order=order,
        )

        self.assertEqual(
            shipment.order,
            order,
        )

        self.assertEqual(
            shipment.shipping_method,
            self.shipping_method,
        )

        # ----------------------------
        # Stock reduction
        # ----------------------------
        self.variant.refresh_from_db()

        self.assertEqual(
            self.variant.stock,
            8,
        )

        # ----------------------------
        # Cart conversion
        # ----------------------------
        self.cart.refresh_from_db()

        self.assertEqual(
            self.cart.status,
            CartStatus.CONVERTED,
        )