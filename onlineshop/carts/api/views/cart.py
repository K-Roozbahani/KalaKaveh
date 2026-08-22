from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from carts.api.schemas.cart import cart_schema
from carts.api.serializers import CartSerializer

from carts.selectors import (
    get_cart_queryset,
    get_active_cart_item_count,
)

from carts.services.cart import (
    clear_cart,
    get_or_create_cart,
)

from carts.services.pricing import (
    calculate_cart_totals,
)

from utils.api.views import BaseGenericViewSet
from utils.session import get_session_key


@cart_schema
class CartViewSet(BaseGenericViewSet):
    """
    API مدیریت سبد خرید.
    """

    permission_classes = [
        AllowAny,
    ]

    pagination_class = None

    # =====================================================
    # Helpers
    # =====================================================

    def get_cart(self):
        """
        دریافت یا ایجاد سبد خرید فعال.

        برای کاربر احراز‌شده، سبد بر اساس User مدیریت می‌شود
        و در صورت وجود Guest Cart مربوط به Session فعلی،
        ادغام به‌صورت Lazy انجام خواهد شد.

        برای کاربر مهمان، سبد بر اساس Session مدیریت می‌شود.
        """

        session_key = get_session_key(
            request=self.request,
        )

        if self.request.user.is_authenticated:
            return get_or_create_cart(
                user=self.request.user,
                session_key=session_key,
            )

        return get_or_create_cart(
            session_key=session_key,
        )

    def cart_response(
        self,
        *,
        cart,
        status_code=status.HTTP_200_OK,
    ):
        """
        آماده‌سازی و نمایش سبد خرید.
        """

        cart = (
            get_cart_queryset()
            .filter(
                pk=cart.pk,
            )
            .first()
        )

        serializer = CartSerializer(
            cart,
            context={
                "request": self.request,
                "pricing": calculate_cart_totals(
                    cart=cart,
                ),
            },
        )

        return Response(
            serializer.data,
            status=status_code,
        )

    # =====================================================
    # API
    # =====================================================

    def list(
        self,
        request,
    ):
        """
        نمایش سبد خرید فعال.
        """

        return self.cart_response(
            cart=self.get_cart(),
        )

    @action(
        detail=False,
        methods=["delete"],
    )
    def clear(
        self,
        request,
    ):
        """
        پاک کردن تمام آیتم‌های سبد خرید.
        """

        cart = self.get_cart()

        clear_cart(
            cart=cart,
        )

        return self.cart_response(
            cart=cart,
        )

    @action(
        detail=False,
        methods=["get"],
    )
    def count(
            self,
            request,
    ):
        """
        دریافت تعداد کالاهای موجود در سبد خرید برای نمایش آیکون.
        """

        session_key = get_session_key(
            request=request,
        )

        item_count = get_active_cart_item_count(
            user=request.user if request.user.is_authenticated else None,
            session_key=session_key,
        )

        return Response(
            {
                "items_count": item_count,
            },
            status=status.HTTP_200_OK,
        )