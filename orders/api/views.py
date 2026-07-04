from rest_framework import status, viewsets, mixins
from rest_framework.decorators import action
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from utils.permissions import IsOwnerOrAdmin

from orders.api.serializers import (
    CreateOrderSerializer,
    OrderDetailSerializer,
    OrderItemSerializer,
    OrderListSerializer,
)

from orders.selectors import (
    get_order_items,
    get_user_order_by_number,
    get_user_orders,
)

from orders.services import (
    create_order_from_cart,
)


class OrderViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    permission_classes = (
        IsAuthenticated,
        IsOwnerOrAdmin,
    )

    lookup_field = "order_number"
    lookup_url_kwarg = "order_number"

    def get_queryset(self):
        return get_user_orders(
            self.request.user,
        )

    def get_serializer_class(self):
        if self.action == "list":
            return OrderListSerializer

        if self.action == "retrieve":
            return OrderDetailSerializer

        if self.action == "create":
            return CreateOrderSerializer

        if self.action == "items":
            return OrderItemSerializer

        if self.action == "latest":
            return OrderDetailSerializer

        return OrderDetailSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()

        serializer = self.get_serializer(
            queryset,
            many=True,
        )

        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        order = get_user_order_by_number(
            request.user,
            kwargs.get("order_number"),
        )

        if not order:
            raise NotFound(
                "سفارش یافت نشد."
            )

        self.check_object_permissions(
            request,
            order,
        )

        serializer = self.get_serializer(
            order,
        )

        return Response(
            serializer.data,
        )

    def items(self, request, *args, **kwargs):
        order = get_user_order_by_number(
            request.user,
            kwargs.get("order_number"),
        )

        if not order:
            raise NotFound(
                "سفارش یافت نشد."
            )

        self.check_object_permissions(
            request,
            order,
        )

        serializer = OrderItemSerializer(
            get_order_items(order),
            many=True,
        )

        return Response(
            serializer.data,
        )