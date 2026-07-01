from django.urls import reverse

from rest_framework import mixins
from rest_framework import status
from rest_framework import viewsets

from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from orders.selectors import get_user_order_by_number

from payments.selectors import get_user_payments

from payments.serializers import (
    PaymentCreateSerializer,
    PaymentDetailSerializer,
    PaymentListSerializer,
)

from payments.services.callback import process_gateway_callback
from payments.services.payment import create_payment
from payments.services.validators import validate_order_exists


class PaymentViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    """
    مدیریت پرداخت‌های کاربر.
    """

    permission_classes = (
        IsAuthenticated,
    )

    def get_queryset(self):
        return get_user_payments(
            self.request.user,
        )

    def get_serializer_class(self):
        if self.action == "create":
            return PaymentCreateSerializer

        if self.action == "retrieve":
            return PaymentDetailSerializer

        return PaymentListSerializer

    def create(
        self,
        request,
        *args,
        **kwargs,
    ):
        serializer = self.get_serializer(
            data=request.data,
        )
        serializer.is_valid(
            raise_exception=True,
        )

        order = get_user_order_by_number(
            user=request.user,
            order_number=serializer.validated_data[
                "order_number"
            ],
        )

        validate_order_exists(order)

        callback_url = request.build_absolute_uri(
            reverse(
                "payments:callback",
            )
        )

        result = create_payment(
            order=order,
            gateway_type=serializer.validated_data[
                "gateway"
            ],
            callback_url=callback_url,
        )

        return Response(
            {
                "payment_url": result[
                    "payment_url"
                ],
                "authority": result[
                    "payment"
                ].authority,
            },
            status=status.HTTP_201_CREATED,
        )


class PaymentCallbackView(APIView):
    """
    Callback پرداخت.
    """

    authentication_classes = ()
    permission_classes = ()

    def get(self, request):
        authority = request.query_params.get(
            "Authority",
        )

        # اعتبارسنجی پارامترهای HTTP
        if not authority:
            raise ValidationError(
                {
                    "Authority": [
                        "This query parameter is required."
                    ]
                }
            )

        payment = process_gateway_callback(
            authority=authority,
        )

        serializer = PaymentDetailSerializer(
            payment,
        )

        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )