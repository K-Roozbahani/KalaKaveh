# cart/views.py

from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _ # برای ترجمه پیام ها
from rest_framework import viewsets, status, mixins
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import action

from carts.models import Cart, CartItem, CartItemAttribute
from products.models import Product # فرض می‌کنیم مدل Product در این اپلیکیشن است
from carts.api.serializer import (
    CartDetailSerializer,
    AddToCartSerializer,
    UpdateCartItemSerializer,
    CartItemAttributeSerializer # برای نمایش attributes در صورت نیاز
)
# فرض می‌کنیم این permission در permissions.py تعریف شده است
# from .permissions import IsOwnerOrAdminOrReadOnly
# برای این مثال، یک permission ساده تر IsAuthenticated یا AllowAny را استفاده می‌کنیم،
# اما در پروژه واقعی، permission سفارشی شما باید اینجا قرار گیرد.
from rest_framework.permissions import IsAuthenticated, AllowAny


# ---------- پیاده‌سازی یک permission سفارشی برای مثال ----------
from rest_framework import permissions

class IsOwnerOrAdmin(permissions.BasePermission):
    """
    اجازه دسترسی فقط به صاحب آبجکت یا ادمین.
    """
    def has_object_permission(self, request, view, obj):
        # اگر کاربر ادمین است، اجازه دسترسی کامل دارد
        if request.user.is_staff:
            return True
        # اگر کاربر، صاحب آبجکت است، اجازه دسترسی دارد
        # فرض می‌کنیم obj دارای فیلد 'user' باشد (مانند Cart)
        return obj.user == request.user

class IsCartOwnerOrAdmin(permissions.BasePermission):
    """
    اجازه دسترسی به سبد خرید فقط برای کاربر صاحب سبد یا ادمین.
    """
    def has_permission(self, request, view):
        # برای اکشن 'list'، اجازه دسترسی عمومی (برای کاربران مهمان) را می‌دهیم.
        # برای سایر اکشن‌ها، باید کاربر احراز هویت شده باشد.
        if view.action == 'list':
            return True
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # obj در اینجا Cart است
        if request.user.is_staff:
            return True
        # اگر سبد خرید مربوط به کاربر است
        return obj.user == request.user and obj.is_active


# ------------------------------------------------------------------


class CartViewSet(viewsets.GenericViewSet):
    """
    ViewSet برای مدیریت سبد خرید کاربران با رعایت کامل استانداردها.
    """
    serializer_class = CartDetailSerializer
    # permission_classes = [IsAuthenticated] # دسترسی پیش فرض، بعدا برای هر اکشن تنظیم می‌شود

    # کوئری ست اولیه با prefetch برای کاهش کوئری ها
    # items__item_attributes را prefetch می‌کنیم تا در هنگام نمایش، کوئری جداگانه نداشته باشیم
    queryset = Cart.objects.prefetch_related('items__item_attributes').select_related('user').all()

    def get_permissions(self):
        """
        تعیین permission classes بر اساس اکشن ViewSet.
        """
        if self.action == 'list':
            # مشاهده سبد خرید برای همه (کاربر احراز هویت شده یا مهمان)
            permission_classes = [AllowAny, IsCartOwnerOrAdmin]
        elif self.action in ['add_item', 'update_item', 'remove_item', 'clear_cart']:
            # عملیات بر روی سبد فقط برای کاربران احراز هویت شده و صاحب سبد
            permission_classes = [IsAuthenticated, IsCartOwnerOrAdmin]
        else:
            # حالت های دیگر
            permission_classes = [IsAuthenticated, IsCartOwnerOrAdmin]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        """
        دریافت سبد خرید فعلی کاربر (احراز هویت شده یا مهمان).
        این متد اطمینان حاصل می‌کند که کاربر فقط به سبد خود دسترسی دارد.
        """
        user = self.request.user
        session_id = self.request.session.session_key

        if user.is_authenticated:
            # برای کاربر احراز هویت شده:
            # ابتدا سبد فعال کاربر را دریافت می‌کنیم.
            # اگر وجود نداشت، یک سبد جدید برای کاربر ایجاد می‌شود.
            cart, created = Cart.objects.get_or_create(user=user, is_active=True)

            # منطق انتقال سبد مهمان به کاربر لاگین شده
            # اگر سبدی که تازه ایجاد شده، دارای session_id بود (یعنی قبلا سبد مهمان بوده)
            # یا اگر سبد موجود، قبلا session_id داشته و کاربر لاگین کرده است
            if created or (cart.session_id and not cart.user): # اگر سبد کاربر قبلا سبد مهمان بوده
                self.merge_guest_cart_if_exists(cart, session_id)

            return cart
        else:
            # برای کاربر مهمان:
            # اگر session_id هنوز ایجاد نشده، آن را فعال می‌کنیم.
            if not session_id:
                self.request.session.save()
                session_id = self.request.session.session_key

            # سبد مربوط به session_id را دریافت یا ایجاد می‌کنیم.
            # Cart.objects.get_or_create به صورت پیش فرض فقط user=None را چک نمی‌کند،
            # پس باید اطمینان حاصل کنیم که سبد مهمان را پیدا کنیم.
            try:
                cart = Cart.objects.get(session_id=session_id, is_active=True, user=None)
                # اگر سبد مهمان یافت شد، اما session_id تغییر کرده بود، آن را آپدیت می‌کنیم
                if cart.session_id != session_id:
                    cart.session_id = session_id
                    cart.save()
                return cart
            except Cart.DoesNotExist:
                # اگر سبد مهمان با این session_id وجود نداشت، یک سبد جدید ایجاد می‌کنیم.
                return Cart.objects.create(session_id=session_id, is_active=True)

    def merge_guest_cart_if_exists(self, user_cart: Cart, guest_session_id: str):
        """
        ادغام سبد خرید مهمان با سبد خرید کاربر احراز هویت شده.
        این عملیات فقط در صورتی انجام می‌شود که سبد مهمان فعال و معتبر باشد.
        """
        if not guest_session_id:
            return # اگر session_id مهمان وجود ندارد، کاری انجام نمی‌دهیم.

        try:
            # سعی می‌کنیم سبد مهمان فعال را پیدا کنیم که متعلق به کاربر نباشد.
            guest_cart = Cart.objects.get(session_id=guest_session_id, is_active=True, user=None)

            # اگر سبد مهمان یافت شد و با سبد کاربر فعلی متفاوت بود:
            if guest_cart and guest_cart != user_cart:
                with transaction.atomic():
                    # انتقال آیتم‌های سبد مهمان به سبد کاربر
                    for item in guest_cart.items.all():
                        # برای هر آیتم، بررسی می‌کنیم که آیا آیتم مشابهی در سبد کاربر وجود دارد
                        # مشابه بودن یعنی: همان محصول، همان قیمت واحد، و همان مجموعه ویژگی‌ها
                        # این بخش برای مدیریت دقیق ویژگی‌ها پیچیده است.
                        existing_item = CartItem.objects.filter(
                            cart=user_cart,
                            product=item.product,
                            unit_price=item.unit_price,
                            product_name_snapshot=item.product_name_snapshot
                        ).first() # فقط اولین مورد مشابه را می‌گیریم

                        if existing_item:
                            # اگر آیتم مشابه یافت شد، تعداد را افزایش می‌دهیم
                            existing_item.quantity += item.quantity
                            # در صورت نیاز، ویژگی‌های اضافه شده به آیتم مهمان را نیز به آیتم کاربر اضافه می‌کنیم
                            # این بخش به نحوه پیاده‌سازی CartItemAttribute بستگی دارد.
                            # برای مثال، اگر attribute_value یک مقدار ساده است:
                            for attr in item.item_attributes.all():
                                if not CartItemAttribute.objects.filter(cart_item=existing_item, attribute_value=attr.attribute_value).exists():
                                    CartItemAttribute.objects.create(
                                        cart_item=existing_item,
                                        attribute_value=attr.attribute_value
                                    )
                            existing_item.save()
                        else:
                            # اگر آیتم مشابهی یافت نشد، یک CartItem جدید در سبد کاربر ایجاد می‌کنیم
                            new_item = CartItem.objects.create(
                                cart=user_cart,
                                product=item.product,
                                quantity=item.quantity,
                                unit_price=item.unit_price,
                                product_name_snapshot=item.product_name_snapshot,
                                # product_image_snapshot=item.product_image_snapshot # اگر snapshot تصویر هم دارید
                            )
                            # کپی کردن ویژگی‌های انتخاب شده از آیتم مهمان
                            for attr in item.item_attributes.all():
                                CartItemAttribute.objects.create(
                                    cart_item=new_item,
                                    attribute_value=attr.attribute_value
                                )

                    # پس از انتقال موفقیت‌آمیز، سبد مهمان را غیرفعال می‌کنیم
                    guest_cart.is_active = False
                    guest_cart.save()

        except Cart.DoesNotExist:
            # اگر سبد مهمان پیدا نشد، مشکلی نیست.
            pass
        except Exception as e:
            # لاگ کردن خطاهای غیرمنتظره حین ادغام سبد
            # در یک پروژه واقعی، این خطاها باید به صورت جدی‌تر مدیریت شوند (مانند sentry)
            print(f"Error merging guest cart: {e}")


    def list(self, request):
        """
        نمایش جزئیات سبد خرید کاربر فعلی (احراز هویت شده یا مهمان).
        """
        cart = self.get_queryset() # دریافت سبد خرید فعلی
        # اطمینان از اینکه CartDetailSerializer می‌تواند با cart کار کند
        serializer = CartDetailSerializer(cart, context={'request': request})
        return Response(serializer.data)

    @action(detail=False, methods=['POST'], url_path='add-item')
    def add_item(self, request):
        """
        افزودن یک محصول به سبد خرید.
        این متد هم برای کاربران احراز هویت شده و هم مهمان کار می‌کند.
        """
        cart = self.get_queryset() # دریافت سبد خرید فعلی (کاربر یا مهمان)
        serializer = AddToCartSerializer(data=request.data, context={'request': request, 'cart': cart})

        if serializer.is_valid():
            product_id = serializer.validated_data['product_id']
            quantity = serializer.validated_data['quantity']
            attribute_values = serializer.validated_data.get('attribute_values', []) # لیست مقادیر ویژگی ها

            try:
                # تلاش برای یافتن محصول
                product = Product.objects.get(id=product_id)

                # بررسی موجودی محصول (اگر پیاده‌سازی شده باشد)
                # if product.stock < quantity:
                #     return Response({"detail": _("موجودی کافی نیست.")}, status=status.HTTP_400_BAD_REQUEST)

                unit_price = serializer.validated_data['unit_price'] # قیمت واحد snapshot شده
                product_name_snapshot = serializer.validated_data['product_name_snapshot'] # نام snapshot شده

                # تلاش برای یافتن CartItem مشابه در سبد خرید فعلی
                # مطابقت دقیق شامل محصول، قیمت واحد و ویژگی‌ها است
                cart_item_qs = CartItem.objects.filter(
                    cart=cart,
                    product_id=product_id,
                    unit_price=unit_price,
                    product_name_snapshot=product_name_snapshot
                )
                # منطق تطابق ویژگی‌ها:
                # ابتدا تعداد ویژگی‌ها را چک می‌کنیم
                if cart_item_qs.exists():
                    # اگر تعداد ویژگی‌ها در درخواست با تعداد ویژگی‌های ذخیره شده در CartItem مطابقت داشت
                    # (نیاز به فیلد یا روشی برای شمارش attribute ها در CartItem داریم)
                    # فعلا فرض می‌کنیم مطابقت قیمت و نام کافی است و تعداد را افزایش می‌دهیم
                    # این قسمت در صورت نیاز به تطابق دقیق ویژگی‌ها باید پیچیده‌تر شود
                    pass # فعلا با موارد قبلی ادغام می‌کنیم

                # گرفتن اولین CartItem مشابه (اگر وجود داشته باشد)
                cart_item = cart_item_qs.first()

                if cart_item:
                    # اگر آیتم مشابه یافت شد، تعداد را افزایش می‌دهیم
                    cart_item.quantity += quantity
                    # اگر ویژگی‌های جدیدی اضافه شده‌اند که قبلا در این CartItem نبوده، آنها را اضافه می‌کنیم
                    # (این بخش نیازمند پیاده‌سازی دقیق‌تر برای CartItemAttribute است)
                    # برای مثال، اگر attribute_value یک مقدار ساده است:
                    for attr_value in attribute_values:
                        # اطمینان حاصل می‌کنیم که این ویژگی قبلا به این CartItem اضافه نشده باشد
                        if not CartItemAttribute.objects.filter(cart_item=cart_item, attribute_value=attr_value).exists():
                            CartItemAttribute.objects.create(
                                cart_item=cart_item,
                                attribute_value=attr_value # فرض می‌شود attr_value همان object ویژگی است
                            )
                    cart_item.save()
                else:
                    # اگر CartItem مشابهی یافت نشد، یک CartItem جدید ایجاد می‌کنیم
                    cart_item = CartItem.objects.create(
                        cart=cart,
                        product=product, # استفاده از object محصول
                        quantity=quantity,
                        unit_price=unit_price,
                        product_name_snapshot=product_name_snapshot,
                        # product_image_snapshot=product.main_image.url if product.main_image else None # snapshot تصویر
                    )
                    # اضافه کردن ویژگی‌های انتخاب شده به CartItemAttribute
                    for attr_value in attribute_values:
                        CartItemAttribute.objects.create(
                            cart_item=cart_item,
                            attribute_value=attr_value
                        )

                # پس از افزودن یا به‌روزرسانی CartItem، کل سبد خرید را دوباره سریالایز می‌کنیم
                # تا اطلاعات کل سبد (قیمت کل، تعداد کل) به‌روز شود.
                updated_cart_serializer = CartDetailSerializer(cart, context={'request': request})
                return Response(updated_cart_serializer.data, status=status.HTTP_200_OK)

            except Product.DoesNotExist:
                return Response({"detail": _("محصول یافت نشد.")}, status=status.HTTP_404_NOT_FOUND)
            except Exception as e:
                # مدیریت خطا برای سایر مشکلات احتمالی
                print(f"Error adding item to cart: {e}")
                return Response({"detail": _("خطایی در افزودن محصول به سبد رخ داد.")}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            # اگر serializer معتبر نبود، خطاهای اعتبارسنجی را برمی‌گردانیم
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    @action(detail=False, methods=['PATCH'], url_path='update-item/(?P<item_id>[0-9]+)')
    def update_item(self, request, item_id):
        """
        به‌روزرسانی تعداد یک آیتم موجود در سبد خرید.
        """
        cart = self.get_queryset()
        try:
            # یافتن CartItem مورد نظر که متعلق به سبد فعلی کاربر باشد
            cart_item = CartItem.objects.get(id=item_id, cart=cart)
        except CartItem.DoesNotExist:
            return Response({"detail": _("آیتم سبد خرید یافت نشد.")}, status=status.HTTP_404_NOT_FOUND)

        # استفاده از serializer برای به‌روزرسانی
        # partial=True امکان به‌روزرسانی جزئی را فراهم می‌کند
        serializer = UpdateCartItemSerializer(instance=cart_item, data=request.data, partial=True, context={'request': request})

        if serializer.is_valid():
            # ذخیره تغییرات (این متد update در serializer را فراخوانی می‌کند)
            serializer.save()

            # اگر تعداد به 0 یا کمتر رسید، آیتم را حذف کن
            if cart_item.quantity <= 0:
                cart_item.delete()
                # اگر سبد خالی شد، خود Cart را هم غیرفعال کن (اختیاری)
                if not cart.items.filter(is_active=True).exists():
                    cart.is_active = False
                    cart.save()

            # بازگرداندن سبد خرید به‌روزرسانی شده
            updated_cart_serializer = CartDetailSerializer(cart, context={'request': request})
            return Response(updated_cart_serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['DELETE'], url_path='remove-item/(?P<item_id>[0-9]+)')
    def remove_item(self, request, item_id):
        """
        حذف یک آیتم کامل از سبد خرید.
        """
        cart = self.get_queryset()
        try:
            # یافتن CartItem مورد نظر
            cart_item = CartItem.objects.get(id=item_id, cart=cart)
            cart_item.delete() # حذف آیتم

            # اگر سبد پس از حذف خالی شد، آن را غیرفعال کن (اختیاری)
            if not cart.items.filter(is_active=True).exists():
                cart.is_active = False
                cart.save()

            # بازگرداندن سبد خرید به‌روزرسانی شده
            updated_cart_serializer = CartDetailSerializer(cart, context={'request': request})
            return Response(updated_cart_serializer.data, status=status.HTTP_200_OK)
        except CartItem.DoesNotExist:
            return Response({"detail": _("آیتم سبد خرید یافت نشد.")}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            print(f"Error removing item from cart: {e}")
            return Response({"detail": _("خطایی در حذف آیتم از سبد رخ داد.")}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    @action(detail=False, methods=['POST'], url_path='clear-cart')
    def clear_cart(self, request):
        """
        حذف تمام آیتم‌های سبد خرید.
        """
        cart = self.get_queryset()
        try:
            # حذف تمام آیتم‌های فعال سبد
            # استفاده از transaction برای اطمینان از اتمیک بودن عملیات
            with transaction.atomic():
                cart.items.filter(is_active=True).delete()
                # غیرفعال کردن کل سبد
                cart.is_active = False
                cart.save()

            # بازگرداندن سبد خرید خالی
            updated_cart_serializer = CartDetailSerializer(cart, context={'request': request})
            return Response(updated_cart_serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            print(f"Error clearing cart: {e}")
            return Response({"detail": _("خطایی در پاک کردن سبد رخ داد.")}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
