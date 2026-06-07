from django.db import models
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model

# from discounts.models import
User = get_user_model()

class Category(models.Model):
    """
    دسته‌بندی محصولات (مثلاً موبایل، پوشاک، لوازم خانگی).
    """
    name = models.CharField(_("نام"), max_length=100)
    slug = models.SlugField(_("اسلاگ"), unique=True, allow_unicode=True, blank=True) # برای URL های خوانا
    parent = models.ForeignKey(
        'self',
        related_name='subcategories',
        verbose_name=_("دسته اصلی"),
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    def save(self, *args, **kwargs):
        if not self.slug: # اگر slug خالی بود، آن را بساز
            self.slug = slugify(self.name, allow_unicode=True)

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class Brand(models.Model):
    """
    اطلاعات برند محصولات.
    """
    name = models.CharField(_("نام برند"), max_length=100)
    slug = models.SlugField(_("اسلاگ"), unique=True, allow_unicode=True, blank=True)  # برای URL های خوانا
    logo = models.ImageField(_("لوگو"), upload_to='brands/logos/', blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.slug: # اگر slug خالی بود، آن را بساز
            self.slug = slugify(self.name, allow_unicode=True)

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class ProductAttribute(models.Model):
    """
    ویژگی‌های مختلف محصولات (مانند رنگ، سایز، حافظه داخلی) که می‌توانند به صورت پویا تعریف شوند.
    """
    name = models.CharField(_("نام ویژگی"), max_length=100)
    description = models.TextField(_("توضیحات"), blank=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    """
    مدل اصلی محصول شامل نام، توضیحات، قیمت، عکس، موجودی، ویژگی‌ها و …
    """
    name = models.CharField(_("نام محصول"), max_length=255)
    slug = models.SlugField(_("اسلاگ"), unique=True, allow_unicode=True, blank=True)  # برای URL های خوانا
    description = models.TextField(_("توضیحات"), blank=True)
    # price = models.DecimalField(_("قیمت"), max_digits=10, decimal_places=2)
    # discount_price = models.DecimalField(_("قیمت با تخفیف"), max_digits=10, decimal_places=2, null=True, blank=True)
    # stock = models.PositiveIntegerField(_("موجودی"), default=0)
    category = models.ForeignKey(Category, related_name='products', on_delete=models.SET_NULL, null=True, blank=True)
    brand = models.ForeignKey(Brand, related_name='products', on_delete=models.SET_NULL, null=True, blank=True)
    # main_image = models.ImageField(_("عکس اصلی"), upload_to='products/images/')
    created_at = models.DateTimeField(_("تاریخ ایجاد"), auto_now_add=True)
    updated_at = models.DateTimeField(_("تاریخ بروزرسانی"), auto_now=True)
    attributes = models.ManyToManyField(ProductAttribute, through='ProductAttributeValue', related_name='products')
    is_active = models.BooleanField(_("موجود"), default=True, )

    def save(self, *args, **kwargs):
        if not self.slug: # اگر slug خالی بود، آن را بساز
            self.slug = slugify(self.name, allow_unicode=True)

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class ProductAttributeValue(models.Model):
    """
    مقادیر واقعی برای ویژگی‌های محصول (مثلاً رنگ “قرمز” برای ویژگی “رنگ”).
    """
    product = models.ForeignKey(Product, related_name='attribute_values', on_delete=models.CASCADE)
    attribute = models.ForeignKey(ProductAttribute, related_name='values', on_delete=models.CASCADE)
    value = models.CharField(_("مقدار"), max_length=255)

    class Meta:
        unique_together = ('product', 'attribute', 'value') # اطمینان از اینکه هر ویژگی برای یک محصول فقط یک بار تعریف شده است

    def __str__(self):
        return f"{self.product.name} - {self.attribute.name}: {self.value}"

class ProductImage(models.Model):
    """
    برای ذخیره چندین عکس برای هر محصول.
    """
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(_("عکس"), upload_to='products/images/')
    alt_text = models.CharField(_("متن جایگزین"), max_length=255, blank=True)

    def __str__(self):
        return f"Image for {self.product.name}"

class ProductVariant(models.Model):
    """
    تنوع محصول
    مثال:
    آیفون 15 مشکی 128 گیگ
    """

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="variants",
        verbose_name=_("محصول")
    )

    sku = models.CharField(
       _("کد انبار (SKU)"),
        max_length=100,
        unique=True
    )

    price = models.PositiveIntegerField(
        _("قیمت"),
    )

    discount_amount = models.PositiveIntegerField(
        _("مبلغ تخفیف"),
        default=0
    )

    final_price = models.PositiveIntegerField(
        _("قیمت نهایی"),
        default=0
    )

    stock = models.PositiveIntegerField(
        _("موجودی"),
        default=0
    )

    attribute_values = models.ManyToManyField(
        ProductAttributeValue,
        through="ProductVariantAttribute",
        related_name="product_variants",
        verbose_name=_("ویژگی‌های تنوع")
    )

    is_active = models.BooleanField(
        _("فعال"),
        default=True
    )

    created_at = models.DateTimeField(
        _("تاریخ ایجاد"),
        auto_now_add=True
    )

    # @property
    # def discount_amount(self):
    #     from discounts.services import get_variant_discount
    #
    #     return get_variant_discount(self)
    #
    # @property
    # def final_price(self):
    #     return max(
    #         self.price - self.discount_amount,
    #         0
    #     )

    def save(self, *args, **kwargs):
        if not self.final_price:
            self.final_price = self.price

        super().save(*args, **kwargs)

    class Meta:
        verbose_name = _("تنوع محصول")
        verbose_name_plural = _("تنوع‌های محصول")

    def __str__(self):
        return f"{self.product.name} - {self.sku}"


class ProductVariantAttribute(models.Model):
    """
    مدل واسط بین تنوع محصول و مقدار ویژگی
    """

    variant = models.ForeignKey(
        ProductVariant,
        on_delete=models.CASCADE,
        related_name="variant_attributes",
        verbose_name=_("تنوع محصول")
    )

    attribute_value = models.ForeignKey(
        ProductAttributeValue,
        on_delete=models.CASCADE,
        related_name="variant_attributes",
        verbose_name=_("مقدار ویژگی")
    )

    class Meta:
        verbose_name = _("ویژگی تنوع محصول")
        verbose_name_plural = _("ویژگی‌های تنوع محصول")
        unique_together = (
            "variant",
            "attribute_value"
        )

    def __str__(self):
        return (
            f"{self.variant.sku} - "
            f"{self.attribute_value.attribute.name}: "
            f"{self.attribute_value.value}"
        )


class VariantImage(models.Model):
    """
    تصاویر مخصوص هر تنوع
    """

    variant = models.ForeignKey(
        ProductVariant,
        on_delete=models.CASCADE,
        related_name="images",
        verbose_name=_("تنوع محصول")
    )

    image = models.ImageField(
        _("تصویر"),
        upload_to="products/variants/"
    )

    is_primary = models.BooleanField(
        _("تصویر اصلی"),
        default=False
    )

    class Meta:
        verbose_name = _("تصویر تنوع محصول")
        verbose_name_plural = _("تصاویر تنوع محصول")

    def __str__(self):
        return f"{_('تصویر')} {self.variant.sku}"



class Review(models.Model):
    """
    برای ثبت نظرات و امتیازات کاربران درباره محصولات.
    """
    product = models.ForeignKey(Product, related_name='reviews', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews', verbose_name=_('کاربر')) # تغییر از user_name به ForeignKey
    comment = models.TextField(_("نظر"), blank=True)
    rating = models.PositiveSmallIntegerField(_("امتیاز"), choices=[(i, i) for i in range(1, 6)]) # امتیاز از 1 تا 5
    created_at = models.DateTimeField(_("تاریخ ایجاد"), auto_now_add=True)

    class Meta:
        unique_together = ('product', 'user')  # اطمینان از اینکه هر کاربر فقط یک نظر و امتیاز میتواند برای هر محصول ثبت کند
        ordering = ['-created_at'] # نمایش جدیدترین نظرها اول

    def __str__(self):
        return f"Review for {self.product.name} by {self.user}"

