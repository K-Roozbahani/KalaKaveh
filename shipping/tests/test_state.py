from django.test import TestCase
from django.core.exceptions import ValidationError

from shipping.constants import ShipmentStatus
from shipping.state import (
    can_transition,
    transition_status,
)

from shipping.tests.factories import (
    create_shipment,
)


class ShipmentStateTest(TestCase):
    def test_can_transition_valid_pending_to_packaged(self):
        result = can_transition(
            ShipmentStatus.PENDING,
            ShipmentStatus.PACKAGED,
        )

        self.assertTrue(result)

    def test_can_transition_invalid_pending_to_shipped(self):
        result = can_transition(
            ShipmentStatus.PENDING,
            ShipmentStatus.SHIPPED,
        )

        self.assertFalse(result)

    def test_transition_pending_to_packaged(self):
        shipment = create_shipment(
            status=ShipmentStatus.PENDING,
        )

        updated = transition_status(
            shipment,
            ShipmentStatus.PACKAGED,
        )

        self.assertEqual(
            updated.status,
            ShipmentStatus.PACKAGED,
        )

    def test_transition_invalid_raises_error(self):
        shipment = create_shipment(
            status=ShipmentStatus.PENDING,
        )

        with self.assertRaises(
            ValidationError,
        ):
            transition_status(
                shipment,
                ShipmentStatus.DELIVERED,
            )

    def test_transition_packaged_to_shipped(self):
        shipment = create_shipment(
            status=ShipmentStatus.PACKAGED,
        )

        updated = transition_status(
            shipment,
            ShipmentStatus.SHIPPED,
        )

        self.assertEqual(
            updated.status,
            ShipmentStatus.SHIPPED,
        )

    def test_transition_packaged_to_canceled(self):
        shipment = create_shipment(
            status=ShipmentStatus.PACKAGED,
        )

        updated = transition_status(
            shipment,
            ShipmentStatus.CANCELED,
        )

        self.assertEqual(
            updated.status,
            ShipmentStatus.CANCELED,
        )

    def test_terminal_state_delivered(self):
        shipment = create_shipment(
            status=ShipmentStatus.SHIPPED,
        )

        updated = transition_status(
            shipment,
            ShipmentStatus.DELIVERED,
        )

        self.assertEqual(
            updated.status,
            ShipmentStatus.DELIVERED,
        )

    def test_terminal_state_returned(self):
        shipment = create_shipment(
            status=ShipmentStatus.SHIPPED,
        )

        updated = transition_status(
            shipment,
            ShipmentStatus.RETURNED,
        )

        self.assertEqual(
            updated.status,
            ShipmentStatus.RETURNED,
        )

    def test_no_transition_from_terminal_state(self):
        shipment = create_shipment(
            status=ShipmentStatus.DELIVERED,
        )

        with self.assertRaises(
            ValidationError,
        ):
            transition_status(
                shipment,
                ShipmentStatus.PACKAGED,
            )