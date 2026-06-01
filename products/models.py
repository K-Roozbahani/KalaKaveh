from django.db import models
from django.utils.translation import gettext_lazy as _

class Category(models.Model):
    """
    دسته‌بندی محصولات (مثلاً موبایل، پوشاک، لوازم خانگی).
    """
    name = models.CharField(_("نام"), max_length=100)
    slug = models.SlugField(_("اسلاگ"), unique=True, allow_unicode=True) # برای URL های خوانا

    def __str__(self):
        return self.name

class Brand(models.Model):
    """
    اطلاعات برند محصولات.
    """
    name = models.CharField(_("نام برند"), max_length=100)
    logo = models.ImageField(_("لوگو"), upload_to='brands/logos/', blank=True, null=True)

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
    description = models.TextField(_("توضیحات"), blank=True)
    price = models.DecimalField(_("قیمت"), max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(_("موجودی"), default=0)
    category = models.ForeignKey(Category, related_name='products', on_delete=models.SET_NULL, null=True, blank=True)
    brand = models.ForeignKey(Brand, related_name='products', on_delete=models.SET_NULL, null=True, blank=True)
    main_image = models.ImageField(_("عکس اصلی"), upload_to='products/images/')
    created_at = models.DateTimeField(_("تاریخ ایجاد"), auto_now_add=True)
    updated_at = models.DateTimeField(_("تاریخ بروزرسانی"), auto_now=True)
    attributes = models.ManyToManyField(ProductAttribute, through='ProductAttributeValue', related_name='products')

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
        unique_together = ('product', 'attribute') # اطمینان از اینکه هر ویژگی برای یک محصول فقط یک بار تعریف شده است

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

class Review(models.Model):
    """
    برای ثبت نظرات و امتیازات کاربران درباره محصولات.
    """
    product = models.ForeignKey(Product, related_name='reviews', on_delete=models.CASCADE)
    user_name = models.CharField(_("نام کاربر"), max_length=100) # در صورت نداشتن سیستم احراز هویت کاربر
    comment = models.TextField(_("نظر"), blank=True)
    rating = models.PositiveSmallIntegerField(_("امتیاز"), choices=[(i, i) for i in range(1, 6)]) # امتیاز از 1 تا 5
    created_at = models.DateTimeField(_("تاریخ ایجاد"), auto_now_add=True)

    class Meta:
        ordering = ['-created_at'] # نمایش جدیدترین نظرها اول

    def __str__(self):
        return f"Review for {self.product.name} by {self.user_name}"

