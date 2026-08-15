from drf_spectacular.utils import (
    extend_schema,
    extend_schema_view,
)

from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from carts.api.serializers import (
    AddCartItemSerializer,
    CartSerializer,
    UpdateCartItemSerializer,
)

from carts.selectors import (
    get_cart_queryset,
    get_cart_item_by_id,
)

from carts.services.cart import (
    add_to_cart,
    get_or_create_cart,
    remove_cart_item,
    update_cart_item,
)

from carts.services.pricing import (
    calculate_cart_totals,
)

from utils.session import (
    get_session_key,
)


@extend_schema_view(
    create=extend_schema(
        tags=["Cart"],
        summary="افزودن آیتم",
        request=AddCartItemSerializer,
        responses={
            status.HTTP_201_CREATED: CartSerializer,
        },
    ),
    partial_update=extend_schema(
        tags=["Cart"],
        summary="ویرایش آیتم",
        request=UpdateCartItemSerializer,
        responses={
            status.HTTP_200_OK: CartSerializer,
        },
    ),
    destroy=extend_schema(
        tags=["Cart"],
        summary="حذف آیتم",
        request=None,
        responses={
            status.HTTP_200_OK: CartSerializer,
        },
    ),
)
class CartItemViewSet(ViewSet):
    """
    API مدیریت آیتم‌های سبد خرید.
    """

    permission_classes = [
        AllowAny,
    ]

    # =====================================================
    # Helpers
    # =====================================================

    def get_cart(self):
        """
        دریافت یا ایجاد سبد خرید فعال.

        برای کاربر احراز هویت‌شده، سبد بر اساس User
        و برای مهمان، سبد بر اساس Session مدیریت می‌شود.
        """

        if self.request.user.is_authenticated:

            return get_or_create_cart(
                user=self.request.user,
            )

        return get_or_create_cart(
            session_key=get_session_key(
                request=self.request,
            ),
        )

    def get_cart_item(self):
        """
        دریافت آیتم متعلق به سبد فعال کاربر جاری.
        """

        if self.request.user.is_authenticated:

            item = get_cart_item_by_id(
                item_id=self.kwargs["pk"],
                user=self.request.user,
            )

        else:

            item = get_cart_item_by_id(
                item_id=self.kwargs["pk"],
                session_key=get_session_key(
                    request=self.request,
                ),
            )

        if item is None:
            raise NotFound()

        return item

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
    # CREATE
    # =====================================================

    def create(
        self,
        request,
    ):
        """
        افزودن محصول به سبد خرید.
        """

        serializer = AddCartItemSerializer(
            data=request.data,
        )

        serializer.is_valid(
            raise_exception=True,
        )

        cart = self.get_cart()

        add_to_cart(
            cart=cart,
            **serializer.validated_data,
        )

        return self.cart_response(
            cart=cart,
            status_code=status.HTTP_201_CREATED,
        )

    # =====================================================
    # UPDATE
    # =====================================================

    def partial_update(
        self,
        request,
        pk=None,
    ):
        """
        بروزرسانی تعداد آیتم سبد خرید.
        """

        item = self.get_cart_item()

        serializer = UpdateCartItemSerializer(
            data=request.data,
        )

        serializer.is_valid(
            raise_exception=True,
        )

        update_cart_item(
            item=item,
            **serializer.validated_data,
        )

        return self.cart_response(
            cart=self.get_cart(),
        )

    # =====================================================
    # DELETE
    # =====================================================

    def destroy(
        self,
        request,
        pk=None,
    ):
        """
        حذف آیتم از سبد خرید.
        """

        item = self.get_cart_item()

        remove_cart_item(
            item=item,
        )

        return self.cart_response(
            cart=self.get_cart(),
        )