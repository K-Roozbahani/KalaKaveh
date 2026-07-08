from rest_framework import mixins
from rest_framework import status
from rest_framework import viewsets

from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action

from checkout.api.serializers import (
    CheckoutSerializer,
    CheckoutConfirmSerializer,
)

from checkout.services import (
    prepare_checkout,
    confirm_checkout,
)


class CheckoutViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    viewsets.GenericViewSet,
):
    """
    مدیریت فرآیند Checkout
    """

    permission_classes = [IsAuthenticated]

    # =====================================================
    # Checkout Summary
    # =====================================================

    def list(self, request, *args, **kwargs):
        """
        دریافت اطلاعات Checkout.
        """

        data = prepare_checkout(
            user=request.user,
        )

        return Response(data)

    # =====================================================
    # Update Checkout
    # =====================================================

    def create(self, request, *args, **kwargs):
        """
        بروزرسانی اطلاعات Checkout.
        """

        serializer = CheckoutSerializer(
            data=request.data,
        )
        serializer.is_valid(raise_exception=True)

        data = prepare_checkout(
            user=request.user,
            **serializer.validated_data,
        )

        return Response(data)

    # =====================================================
    # Confirm Checkout
    # =====================================================

    @action(
        detail=False,
        methods=["post"],
        url_path="confirm",
    )
    def confirm(self, request):
        """
        تایید نهایی Checkout.
        """

        serializer = CheckoutConfirmSerializer(
            data=request.data,
        )
        serializer.is_valid(raise_exception=True)

        payment = confirm_checkout(
            user=request.user,
            callback_url=request.build_absolute_uri(),
            **serializer.validated_data,
        )

        return Response(
            {
                "payment_url": payment.payment_url,
            },
            status=status.HTTP_201_CREATED,
        )