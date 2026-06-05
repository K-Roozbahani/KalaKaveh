from django.contrib import admin
from django.utils.html import format_html
from products.models import (
    Category, Brand, Product, ProductAttribute,
    ProductAttributeValue, ProductImage,ProductVariant,
    ProductVariantAttribute,VariantImage, Review
)


# --- Inlines ---
class ProductAttributeValueInline(admin.TabularInline):
    model = ProductAttributeValue
    extra = 1
    autocomplete_fields = ('attribute',)


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
    # نمایش پیش‌نمایش تصویر در پنل ادمین
    readonly_fields = ('image_preview',)

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="width: 50px; height: 50px;" />', obj.image.url)
        return "No Image"

class ProductVariantInline(admin.TabularInline):
    model = ProductVariant
    extra = 1

    fields = (
        "sku",
        "price",
        "stock",
        "is_active",
    )

    show_change_link = True

class ProductVariantAttributeInline(admin.TabularInline):
    model = ProductVariantAttribute
    extra = 1
    autocomplete_fields = (
        "attribute_value",
    )

class VariantImageInline(admin.TabularInline):
    model = VariantImage
    extra = 1

class ReviewInline(admin.TabularInline):
    model = Review
    extra = 0
    readonly_fields = ('created_at',)


# --- Admins ---

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug', 'parent')
    search_fields = ('name', 'slug')
    list_filter = ('parent',)
    prepopulated_fields = {'slug': ('name',)}
    autocomplete_fields = ('parent',)  # اضافه شده برای سهولت کار


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}


@admin.register(ProductAttribute)
class ProductAttributeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug', 'category', 'price', 'discount_price', 'stock', 'is_active',)
    list_editable = ('slug', 'price', 'discount_price', 'stock', 'is_active')
    search_fields = ('name', 'category__name', 'brand__name')
    list_filter = ('is_active', 'category', 'brand')
    readonly_fields = ('created_at', 'updated_at')
    autocomplete_fields = ('category', 'brand')
    inlines = [ProductAttributeValueInline, ProductImageInline, ReviewInline]
    prepopulated_fields = {'slug': ('name',)}


@admin.register(ProductAttributeValue)
class ProductAttributeValueAdmin(admin.ModelAdmin):
    list_display = ('product', 'attribute', 'value')
    autocomplete_fields = ('product', 'attribute')
    search_fields = ('value',)


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('product', 'image_tag')
    autocomplete_fields = ('product',)

    def image_tag(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="width: 45px; height: 45px;" />', obj.image.url)
        return None

@admin.register(ProductVariant)
class ProductVariantAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "product",
        "sku",
        "price",
        "stock",
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

    inlines = [
        ProductVariantAttributeInline,
        VariantImageInline,
    ]

@admin.register(ProductVariantAttribute)
class ProductVariantAttributeAdmin(admin.ModelAdmin):
    list_display = (
        "variant",
        "attribute_value",
    )

    autocomplete_fields = (
        "variant",
        "attribute_value",
    )

@admin.register(VariantImage)
class VariantImageAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "variant",
        "is_primary",
    )

    list_filter = (
        "is_primary",
    )

    autocomplete_fields = (
        "variant",
    )


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('product', 'user', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')
    autocomplete_fields = ('product',)
