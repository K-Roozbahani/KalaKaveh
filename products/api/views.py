from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from utils.permissions import IsOwnerOrReadOnly

from .models import (
    Category, Brand, ProductAttribute, Product,
    ProductAttributeValue, ProductImage, Review
)
from .serializers import (
    CategorySerializer, BrandSerializer, ProductAttributeSerializer,
    ProductSerializer, ProductImageSerializer, ReviewCreateSerializer
)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class BrandViewSet(viewsets.ModelViewSet):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer


class ProductAttributeViewSet(viewsets.ModelViewSet):
    queryset = ProductAttribute.objects.all()
    serializer_class = ProductAttributeSerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_queryset(self):
        """
        بهینه‌سازی کوئری‌ها برای جلوگیری از مشکل N+1
        و همچنین فیلتر کردن محصولات فعال
        """
        queryset = Product.objects.select_related('category', 'brand').prefetch_related(
            'images',
            'attribute_values',
            'attribute_values__attribute'
        ).filter(is_active=True)

        # امکان فیلتر بر اساس دسته‌بندی از طریق URL (مثلاً ?category=1)
        category_id = self.request.query_params.get('category')
        if category_id:
            queryset = queryset.filter(category_id=category_id)

        return queryset

    def perform_create(self, serializer):
        # اینجا می‌توانید منطق خاصی برای هنگام ساخت محصول اضافه کنید
        serializer.save()

    @action(detail=True, methods=['post'], url_path='add-review')
    def add_review(self, request, pk=None):
        """
        اگر کاربر قبلاً برای این محصول نظر داده باشد، نظرش بروزرسانی می‌شود.
        در غیر این صورت، یک نظر جدید ثبت می‌شود.
        """
        product = self.get_object()
        user = request.user

        # بررسی وجود نظر قبلی برای این کاربر و این محصول خاص
        existing_review = Review.objects.filter(product=product, user=user).first()

        # داده‌های ارسالی (فقط comment و rating)
        data = request.data

        if existing_review:
            # حالت ۱: بروزرسانی نظر قبلی (Update)
            # استفاده از serializer برای اعتبارسنجی داده‌های جدید
            serializer = ReviewCreateSerializer(existing_review, data=data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({
                    'status': 'نظر شما با موفقیت بروزرسانی شد.',
                    'data': serializer.data
                }, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        else:
            # حالت ۲: ثبت نظر جدید (Create)
            serializer = ReviewCreateSerializer(data=data)
            if serializer.is_valid():
                # ذخیره با اختصاص دادن خودکار محصول و کاربر
                serializer.save(product=product, user=user)
                return Response({
                    'status': 'نظر شما با موفقیت ثبت شد.'
                }, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['get'], url_path='images')
    def product_images(self, request, pk=None):
        """
        نمایش لیست عکس‌های یک محصول به صورت جداگانه
        مثال: GET /api/products/1/images/
        """
        product = self.get_object()
        images = product.images.all()
        serializer = ProductImageSerializer(images, many=True)
        return Response(serializer.data)


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewCreateSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]  # IsOwnerOrReadOnly همان کلاسی است که در پاسخ قبل ساختیم

    def create(self, request, *args, **kwargs):
        """
        اگر کاربر نظر داده باشد، آن را بروزرسانی می‌کند.
        اگر نداده باشد، نظر جدید ایجاد می‌کند.
        """
        product_id = request.data.get('product')
        user = request.user

        if not product_id:
            return Response({"error": "شناسه محصول (product) الزامی است."}, status=status.HTTP_400_BAD_REQUEST)

        # داده‌های ارسالی از کاربر (فقط نظر و امتیاز)
        comment = request.data.get('comment')
        rating = request.data.get('rating')

        # بررسی وجود نظر قبلی برای این کاربر و این محصول
        review_queryset = Review.objects.filter(product_id=product_id, user=user)

        if review_queryset.exists():
            # حالت بروزرسانی (Update)
            review = review_queryset.first()
            # مقداردهی فیلدها با داده‌های جدید
            review.comment = comment if comment is not None else review.comment
            review.rating = rating if rating is not None else review.rating
            review.save()

            # استفاده از سریالایزر برای برگرداندن دیتای آپدیت شده با فرمت استاندارد
            serializer = self.get_serializer(review)
            return Response({
                "message": "نظر شما با موفقیت بروزرسانی شد.",
                "data": serializer.data
            }, status=status.HTTP_200_OK)
        else:
            # حالت ایجاد (Create)
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save(product_id=product_id, user=user)
            return Response({
                "message": "نظر شما با موفقیت ثبت شد.",
                "data": serializer.data
            }, status=status.HTTP_201_CREATED)

    def get_queryset(self):
        return Review.objects.all()
