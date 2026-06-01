from django.contrib import admin
from django.contrib.auth import get_user_model
from .models import Address

# ۱. تعریف Inline برای آدرس‌ها
class AddressInline(admin.TabularInline): # استفاده از TabularInline برای نمایش فشرده و ردیفی
    model = Address
    extra = 1  # تعداد ردیف‌های خالی که برای اضافه کردن آدرس جدید در همان صفحه نمایش داده می‌شود
    max_num = 5 # حداکثر تعداد آدرس‌هایی که می‌توان در این صفحه اضافه کرد



class AdminUser(admin.ModelAdmin):
    fields = ("first_name", "last_name", "phone_number", "email", "last_login")
    inlines = (AddressInline,) # اضافه کردن آدرس‌ها به صفحه کاربر
admin.site.register(get_user_model(), AdminUser)

@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    # ۱. فیلدهایی که در لیست اصلی (Table View) نمایش داده می‌شوند
    list_display = ('title', 'user', 'city', 'state', 'phone_number', 'created_at')

    # ۲. فیلدهایی که در پنل سمت راست برای فیلتر کردن سریع استفاده می‌شوند
    list_filter = ('state', 'city', 'created_at')

    # ۳. فیلدهایی که می‌توان با تایپ کردن در نوار جستجو آن‌ها را پیدا کرد
    # توجه: برای جستجو در فیلد ForeignKey (مثل user) باید از نام رابطه استفاده کنید
    search_fields = ('title', 'user__username', 'user__email', 'city', 'street', 'postal_code')

    # ۴. تعیین اینکه کدام فیلدها در صفحه ویرایش قابل کلیک یا مشاهده باشند
    # (در اینجا ما می‌خواهیم وقتی روی نام کاربر کلیک شد، به صفحه کاربر برود)
    list_display_links = ('title', 'user')

    # ۵. فیلدهایی که در صفحه ویرایش به صورت دسته‌بندی شده یا مرتب نمایش داده شوند
    # (اختیاری: می‌توانید از fieldsets برای گروه‌بندی استفاده کنید)
    fieldsets = (
        ('اطلاعات اصلی آدرس', {
            'fields': ('title', 'user', 'phone_number')
        }),
        ('جزئیات جغرافیایی', {
            'fields': ('state', 'city', 'street', 'address_details')
        }),
        ('اطلاعات امنیتی/سیستمی', {
            'fields': ('postal_code',),
            'classes': ('collapse',)  # این بخش را به صورت پیش‌فرض جمع شده (Collapsed) نمایش می‌دهد
        }),
    )

    # ۶. نمایش آدرس‌ها به صورت مرتب شده (مثلاً جدیدترین‌ها در بالا)
    ordering = ('-created_at',)

    # ۷. اضافه کردن قابلیت مشاهده سریع (در صورت نیاز)
    # اگر می‌خواهید مثلاً شماره تماس را سریع ببینید، این کار در list_display انجام شده است.
