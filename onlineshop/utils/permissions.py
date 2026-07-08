from rest_framework import permissions

class IsOwnerOrAdmin(permissions.BasePermission):
    """
    اجازه دسترسی فقط به:
    - مالک آبجکت (owner)
    - یا admin / staff
    """

    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):

        # Admin full access
        if request.user.is_staff or request.user.is_superuser:
            return True

        # Owner access (برای Address و مدل‌هایی که user دارند)
        return getattr(obj, "user", None) == request.user

# class IsOwnerOrAdmin(permissions.BasePermission):
#     """
#     اجازه دسترسی به مالک آبجکت یا ادمین‌ها را می‌دهد.
#     """
#     def has_object_permission(self, request, view, obj):
#         # ادمین‌ها همیشه دسترسی دارند
#         if request.user.is_staff:
#             return True
#
#         # کاربر فقط می‌تواند آبجکت خودش را ویرایش/مشاهده کند
#         return obj == request.user

# یک Permission سفارشی برای اینکه هر کس فقط نظر خودش را ویرایش کند
class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    فقط صاحب نظر اجازه ویرایش یا حذف دارد. بقیه فقط می‌توانند بخوانند.
    """
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS: # GET, HEAD, OPTIONS
            return True
        return obj.user == request.user


class IsStaffUser(permissions.BasePermission):

    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_staff
        )