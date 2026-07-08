from abc import ABC
from abc import abstractmethod

from payments.constants import GatewayType


class BaseGateway(ABC):
    """
    رابط پایه درگاه پرداخت.
    """

    @abstractmethod
    def request_payment(
        self,
        *,
        amount,
        description,
        callback_url,
    ):
        """
        ایجاد درخواست پرداخت.
        """
        raise NotImplementedError

    @abstractmethod
    def verify_payment(
        self,
        *,
        authority,
        amount,
    ):
        """
        بررسی وضعیت پرداخت.
        """
        raise NotImplementedError



class ZarinpalGateway(BaseGateway):
    """
    درگاه زرین پال.
    """

    def request_payment(
        self,
        *,
        amount,
        description,
        callback_url,
    ):
        return {
            "authority": "TEST_AUTHORITY",
            "payment_url": (
                "https://www.zarinpal.com/pg/StartPay/"
                "TEST_AUTHORITY"
            ),
        }

    def verify_payment(
        self,
        *,
        authority,
        amount,
    ):
        return {
            "success": True,
            "ref_id": "123456789",
        }


def get_gateway(gateway_type):
    """
    دریافت نمونه درگاه پرداخت.
    """

    gateways = {
        GatewayType.ZARINPAL: ZarinpalGateway,
    }

    gateway_class = gateways.get(
        gateway_type,
    )

    if gateway_class is None:
        raise ValueError(
            "Invalid gateway."
        )

    return gateway_class()