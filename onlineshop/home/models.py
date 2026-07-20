from django.db import models
from django.utils.translation import gettext_lazy as _

from home.constants import HomeSectionLayout, HomeSectionType


class HomeSection(models.Model):
    """
    سکشن‌های صفحه اصلی
    """

    title = models.CharField(
        verbose_name=_("عنوان"),
        max_length=255,
        blank=True,
    )

    section_type = models.CharField(
        verbose_name=_("نوع سکشن"),
        max_length=50,
        choices=HomeSectionType.choices,
        db_index=True,
    )

    layout = models.CharField(
        verbose_name=_("نوع نمایش"),
        max_length=30,
        choices=HomeSectionLayout.choices,
    )

    config = models.JSONField(
        verbose_name=_("تنظیمات"),
        default=dict,
        blank=True,
    )

    order = models.PositiveSmallIntegerField(
        verbose_name=_("ترتیب نمایش"),
        default=1,
        db_index=True,
    )

    is_active = models.BooleanField(
        verbose_name=_("فعال"),
        default=True,
        db_index=True,
    )

    created_at = models.DateTimeField(
        verbose_name=_("تاریخ ایجاد"),
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        verbose_name=_("تاریخ بروزرسانی"),
        auto_now=True,
    )

    class Meta:
        verbose_name = _("سکشن صفحه اصلی")
        verbose_name_plural = _("سکشن‌های صفحه اصلی")
        ordering = ("order",)

    def __str__(self):
        return self.title or self.get_section_type_display()


class HeroSlide(models.Model):
    """
    اسلایدهای بخش Hero
    """

    section = models.ForeignKey(
        HomeSection,
        on_delete=models.CASCADE,
        related_name="hero_slides",
        verbose_name=_("سکشن"),
    )

    title = models.CharField(
        verbose_name=_("عنوان"),
        max_length=255,
    )

    subtitle = models.CharField(
        verbose_name=_("زیرعنوان"),
        max_length=255,
        blank=True,
    )

    desktop_image = models.ImageField(
        verbose_name=_("تصویر دسکتاپ"),
        upload_to="home/hero/",
    )

    mobile_image = models.ImageField(
        verbose_name=_("تصویر موبایل"),
        upload_to="home/hero/",
        blank=True,
    )

    button_text = models.CharField(
        verbose_name=_("متن دکمه"),
        max_length=100,
        blank=True,
    )

    button_url = models.CharField(
        verbose_name=_("آدرس دکمه"),
        max_length=500,
        blank=True,
    )

    order = models.PositiveSmallIntegerField(
        verbose_name=_("ترتیب"),
        default=1,
    )

    is_active = models.BooleanField(
        verbose_name=_("فعال"),
        default=True,
    )

    class Meta:
        ordering = ("order",)


class Banner(models.Model):
    """
    بنرهای صفحه اصلی
    """

    section = models.ForeignKey(
        HomeSection,
        on_delete=models.CASCADE,
        related_name="banners",
        verbose_name=_("سکشن"),
    )

    title = models.CharField(
        verbose_name=_("عنوان"),
        max_length=255,
        blank=True,
    )

    desktop_image = models.ImageField(
        verbose_name=_("تصویر دسکتاپ"),
        upload_to="home/banner/",
    )

    mobile_image = models.ImageField(
        verbose_name=_("تصویر موبایل"),
        upload_to="home/banner/",
        blank=True,
    )

    url = models.CharField(
        verbose_name=_("لینک"),
        max_length=500,
        blank=True,
    )

    order = models.PositiveSmallIntegerField(
        verbose_name=_("ترتیب"),
        default=1,
    )

    is_active = models.BooleanField(
        verbose_name=_("فعال"),
        default=True,
    )

    class Meta:
        ordering = ("order",)

class BaseHomeSectionItem(models.Model):
    """
    مدل پایه برای آیتم‌های سکشن صفحه اصلی
    """

    section = models.ForeignKey(
        HomeSection,
        on_delete=models.CASCADE,
        verbose_name=_("سکشن"),
    )

    order = models.PositiveSmallIntegerField(
        verbose_name=_("ترتیب نمایش"),
        default=1,
        db_index=True,
    )

    class Meta:
        abstract = True
        ordering = ("order",)



class HomeSectionProduct(BaseHomeSectionItem):
    """
    محصولات انتخابی سکشن
    """

    product = models.ForeignKey(
        "products.Product",
        on_delete=models.CASCADE,
        related_name="+",
        verbose_name=_("محصول"),
    )

    class Meta(BaseHomeSectionItem.Meta):
        verbose_name = _("محصول سکشن")
        verbose_name_plural = _("محصولات سکشن")
        constraints = [
            models.UniqueConstraint(
                fields=("section", "product"),
                name="unique_home_section_product",
            )
        ]


class HomeSectionCategory(BaseHomeSectionItem):
    """
    دسته‌بندی‌های انتخابی سکشن
    """

    category = models.ForeignKey(
        "products.Category",
        on_delete=models.CASCADE,
        related_name="+",
        verbose_name=_("دسته‌بندی"),
    )

    class Meta(BaseHomeSectionItem.Meta):
        verbose_name = _("دسته‌بندی سکشن")
        verbose_name_plural = _("دسته‌بندی‌های سکشن")
        constraints = [
            models.UniqueConstraint(
                fields=("section", "category"),
                name="unique_home_section_category",
            )
        ]


class HomeSectionBrand(BaseHomeSectionItem):
    """
    برندهای انتخابی سکشن
    """

    brand = models.ForeignKey(
        "products.Brand",
        on_delete=models.CASCADE,
        related_name="+",
        verbose_name=_("برند"),
    )

    class Meta(BaseHomeSectionItem.Meta):
        verbose_name = _("برند سکشن")
        verbose_name_plural = _("برندهای سکشن")
        constraints = [
            models.UniqueConstraint(
                fields=("section", "brand"),
                name="unique_home_section_brand",
            )
        ]