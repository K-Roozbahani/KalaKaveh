from django.contrib import admin
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

from django import forms
from django_ckeditor_5.widgets import CKEditor5Widget

from products.models import (
    Category,
    Brand,
    Product,
    ProductAttribute,
    ProductAttributeValue,
    ProductImage,
    ProductVariant,
    ProductVariantAttribute,
    VariantImage,
    Review,
)


# ==========================================================
# Actions
# ==========================================================

@admin.action(description=_("تایید نظرات انتخاب شده"))
def approve_reviews(
    modeladmin,
    request,
    queryset,
):
    queryset.update(
        is_valid=True,
    )


@admin.action(description=_("رد نظرات انتخاب شده"))
def reject_reviews(
    modeladmin,
    request,
    queryset,
):
    queryset.update(
        is_valid=False,
    )


# ==========================================================
# Inline Admins
# ==========================================================

class ProductAttributeValueInline(admin.TabularInline):
    """
    ویژگی‌های محصول
    """

    model = ProductAttributeValue
    extra = 1

    autocomplete_fields = (
        "attribute",
    )


class ProductImageInline(admin.TabularInline):
    """
    تصاویر محصول
    """

    model = ProductImage
    extra = 1

    readonly_fields = (
        "image_preview",
    )

    fields = (
        "image",
        "alt_text",
        "image_preview",
    )

    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="max-height:70px;" />',
                obj.image.url,
            )

        return "-"

    image_preview.short_description = _("پیش نمایش")


class ProductVariantInline(admin.TabularInline):
    """
    تنوع‌های محصول
    """

    model = ProductVariant

    extra = 1

    fields = (
        "sku",
        "price",
        "discount_amount",
        "final_price",
        "stock",
        "is_active",
    )

    readonly_fields = (
        "discount_amount",
        "final_price",
    )

    show_change_link = True


class ProductVariantAttributeInline(admin.TabularInline):
    """
    ویژگی‌های تنوع
    """

    model = ProductVariantAttribute

    extra = 1

    autocomplete_fields = (
        "attribute_value",
    )


class VariantImageInline(admin.TabularInline):
    """
    تصاویر تنوع
    """

    model = VariantImage

    extra = 1


class ReviewInline(admin.TabularInline):
    """
    نظرات محصول
    """

    model = Review

    extra = 0

    fields = (
        "user",
        "rating",
        "is_valid",
        "created_at",
    )

    readonly_fields = (
        "created_at",
    )

    autocomplete_fields = (
        "user",
    )

    show_change_link = True


# ==========================================================
# Category
# ==========================================================

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "name",
        "slug",
        "parent",
    )

    search_fields = (
        "name",
        "slug",
    )

    list_filter = (
        "parent",
    )

    ordering = (
        "name",
    )

    autocomplete_fields = (
        "parent",
    )

    prepopulated_fields = {
        "slug": (
            "name",
        ),
    }

    list_per_page = 30

    show_full_result_count = False


# ==========================================================
# Brand
# ==========================================================

@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "name",
        "slug",
    )

    search_fields = (
        "name",
        "slug",
    )

    ordering = (
        "name",
    )

    prepopulated_fields = {
        "slug": (
            "name",
        ),
    }

    list_per_page = 30

    show_full_result_count = False


# ==========================================================
# Product Attribute
# ==========================================================

@admin.register(ProductAttribute)
class ProductAttributeAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "name",
    )

    search_fields = (
        "name",
    )

    ordering = (
        "name",
    )

    list_per_page = 30

    show_full_result_count = False


# ==========================================================
# Product
# ==========================================================

class ProductAdminForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = "__all__"

        widgets = {
            "description": CKEditor5Widget(
                config_name="default",
            ),
        }


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):

    form = ProductAdminForm

    list_display = (
        "id",
        "name",
        "brand",
        "category",
        "is_active",
        "created_at",
    )

    list_editable = (
        "is_active",
    )

    list_filter = (
        "is_active",
        "category",
        "brand",
    )

    search_fields = (
        "name",
        "category__name",
        "brand__name",
    )

    ordering = (
        "-created_at",
    )

    date_hierarchy = "created_at"

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    autocomplete_fields = (
        "category",
        "brand",
    )

    prepopulated_fields = {
        "slug": (
            "name",
        ),
    }

    inlines = (
        ProductAttributeValueInline,
        ProductImageInline,
        ProductVariantInline,
        ReviewInline,
    )

    list_per_page = 30

    show_full_result_count = False


# ==========================================================
# Product Attribute Value
# ==========================================================

@admin.register(ProductAttributeValue)
class ProductAttributeValueAdmin(admin.ModelAdmin):

    list_display = (
        "product",
        "attribute",
        "value",
    )

    search_fields = (
        "value",
        "product__name",
        "attribute__name",
    )

    autocomplete_fields = (
        "product",
        "attribute",
    )

    list_per_page = 30

    show_full_result_count = False


# ==========================================================
# Product Images
# ==========================================================

@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "product",
        "image_tag",
    )

    autocomplete_fields = (
        "product",
    )

    readonly_fields = (
        "image_tag",
    )

    list_per_page = 30

    show_full_result_count = False

    def image_tag(self, obj):

        if obj.image:
            return format_html(
                '<img src="{}" style="max-height:60px;" />',
                obj.image.url,
            )

        return "-"

    image_tag.short_description = _("تصویر")



# ==========================================================
# Product Variant
# ==========================================================

@admin.register(ProductVariant)
class ProductVariantAdmin(admin.ModelAdmin):
    """
    مدیریت تنوع محصولات
    """

    list_display = (
        "id",
        "product",
        "sku",
        "price",
        "discount_amount",
        "final_price",
        "stock",
        "is_active",
    )

    list_editable = (
        "is_active",
    )

    list_filter = (
        "is_active",
        "product",
    )

    search_fields = (
        "sku",
        "product__name",
    )

    autocomplete_fields = (
        "product",
    )

    readonly_fields = (
        "discount_amount",
        "final_price",
        "created_at",
    )

    ordering = (
        "-created_at",
    )

    date_hierarchy = "created_at"

    inlines = (
        ProductVariantAttributeInline,
        VariantImageInline,
    )

    list_per_page = 30

    show_full_result_count = False


# ==========================================================
# Product Variant Attribute
# ==========================================================

@admin.register(ProductVariantAttribute)
class ProductVariantAttributeAdmin(admin.ModelAdmin):
    """
    ویژگی‌های تنوع محصول
    """

    list_display = (
        "variant",
        "attribute_value",
    )

    search_fields = (
        "variant__sku",
        "attribute_value__value",
        "attribute_value__attribute__name",
    )

    autocomplete_fields = (
        "variant",
        "attribute_value",
    )

    list_per_page = 30

    show_full_result_count = False


# ==========================================================
# Variant Images
# ==========================================================

@admin.register(VariantImage)
class VariantImageAdmin(admin.ModelAdmin):
    """
    تصاویر تنوع محصول
    """

    list_display = (
        "id",
        "variant",
        "is_primary",
        "image_preview",
    )

    list_editable = (
        "is_primary",
    )

    list_filter = (
        "is_primary",
    )

    autocomplete_fields = (
        "variant",
    )

    readonly_fields = (
        "image_preview",
    )

    list_per_page = 30

    show_full_result_count = False

    def image_preview(self, obj):

        if obj.image:
            return format_html(
                '<img src="{}" style="max-height:60px;" />',
                obj.image.url,
            )

        return "-"

    image_preview.short_description = _("پیش نمایش")


# ==========================================================
# Reviews
# ==========================================================

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    """
    مدیریت نظرات کاربران
    """

    list_display = (
        "id",
        "product",
        "user",
        "rating",
        "is_valid",
        "created_at",
    )

    list_editable = (
        "is_valid",
    )

    list_filter = (
        "is_valid",
        "rating",
        "created_at",
    )

    search_fields = (
        "product__name",
        "user__phone_number",
        "comment",
    )

    autocomplete_fields = (
        "product",
        "user",
    )

    readonly_fields = (
        "created_at",
    )

    ordering = (
        "-created_at",
    )

    date_hierarchy = "created_at"

    actions = (
        approve_reviews,
        reject_reviews,
    )

    list_per_page = 30

    show_full_result_count = False

    fieldsets = (
        (
            _("اطلاعات نظر"),
            {
                "fields": (
                    "product",
                    "user",
                    "rating",
                    "comment",
                )
            },
        ),
        (
            _("وضعیت"),
            {
                "fields": (
                    "is_valid",
                    "created_at",
                )
            },
        ),
    )