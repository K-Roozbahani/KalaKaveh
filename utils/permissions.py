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