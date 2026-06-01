from django.contrib import admin
from django.utils.html import format_html
from .models import (
    Category, Brand, Product, ProductAttribute,
    ProductAttributeValue, ProductImage, Review
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


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('product', 'image_tag')
    autocomplete_fields = ('product',)

    def image_tag(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="width: 45px; height: 45px;" />', obj.image.url)
        return None


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('product', 'user_name', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')
    autocomplete_fields = ('product',)
