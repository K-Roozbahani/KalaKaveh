from rest_framework import permissions

class IsOwnerOrAdmin(permissions.BasePermission):
    """
    اجازه دسترسی به مالک آبجکت یا ادمین‌ها را می‌دهد.
    """
    def has_object_permission(self, request, view, obj):
        # ادمین‌ها همیشه دسترسی دارند
        if request.user.is_staff:
            return True

        # کاربر فقط می‌تواند آبجکت خودش را ویرایش/مشاهده کند
        return obj == request.user

# یک Permission سفارشی برای اینکه هر کس فقط نظر خودش را ویرایش کند
class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    فقط صاحب نظر اجازه ویرایش یا حذف دارد. بقیه فقط می‌توانند بخوانند.
    """
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS: # GET, HEAD, OPTIONS
            return True
        return obj.user == request.user