from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from utils.permissions import IsOwnerOrAdmin

from addresses.models import Address
from addresses import selectors, services

from addresses.api.serializers import (
    AddressListSerializer,
    AddressDetailSerializer,
    AddressCreateSerializer,
    AddressUpdateSerializer,
)


class AddressViewSet(viewsets.ModelViewSet):
    """
    مدیریت آدرس‌های کاربر
    """
    permission_classes = (IsAuthenticated, IsOwnerOrAdmin)


    def get_queryset(self):
        return selectors.get_user_addresses(user=self.request.user)


    def get_serializer_class(self):
        if self.action == "list":
            return AddressListSerializer

        if self.action == "retrieve":
            return AddressDetailSerializer

        if self.action == "create":
            return AddressCreateSerializer

        if self.action in ["update", "partial_update"]:
            return AddressUpdateSerializer

        return AddressDetailSerializer


    def perform_create(self, serializer):
        services.create_address(
            user=self.request.user,
            **serializer.validated_data,
        )


    def perform_update(self, serializer):
        address = self.get_object()

        services.update_address(
            address=address,
            **serializer.validated_data,
        )


    def perform_destroy(self, instance):
        services.delete_address(address=instance)


    @action(detail=True, methods=["post"])
    def set_default(self, request, pk=None):
        address = self.get_object()

        updated = services.set_default_address(address=address)

        return Response(
            {
                "message": "آدرس پیش‌فرض تغییر کرد",
                "address_id": updated.id,
            },
            status=status.HTTP_200_OK,
        )


