"""
مدیریت CSRF برای احراز هویت مبتنی بر Cookie.

این ماژول مسئول ایجاد CSRF Cookie برای Frontend است.
CSRF Token توسط Django تولید و در Cookie قرار می‌گیرد
و Frontend آن را برای درخواست‌های حساس در Header ارسال می‌کند.
"""

from django.middleware.csrf import get_token

from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView


class CSRFTokenView(APIView):
    """
    Endpoint دریافت CSRF Token برای Frontend.

    این Endpoint عمومی است و نیاز به احراز هویت ندارد،
    زیرا کاربر ممکن است قبل از Login به CSRF Token نیاز داشته باشد.
    """

    permission_classes = [AllowAny]

    def get(self, request):
        """
        ایجاد CSRF Token و قرار دادن آن در Cookie.
        """

        # --------------------------------------------------
        # ایجاد CSRF Token
        #
        # Django در صورت نبودن Token، آن را ایجاد کرده
        # و در Response به صورت Cookie قرار می‌دهد.
        # --------------------------------------------------

        get_token(request)

        return Response(
            {
                "detail": "CSRF Token با موفقیت ایجاد شد.",
            }
        )