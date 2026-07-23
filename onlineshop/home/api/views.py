from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from home.api.serializers import HomePageSerializer
from home.services import get_home_sections


class HomePageAPIView(APIView):
    """
    دریافت اطلاعات صفحه اصلی فروشگاه.
    """

    authentication_classes = ()
    permission_classes = ()

    def get(self, request):
        """
        دریافت سکشن‌های صفحه اصلی.
        """

        sections = get_home_sections()

        serializer = HomePageSerializer(
            sections,
            context={
                "request": request,
            },
        )

        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )