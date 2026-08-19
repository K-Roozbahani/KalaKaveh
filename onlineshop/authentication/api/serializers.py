from rest_framework import serializers

from django.contrib.auth import get_user_model
from phonenumber_field.serializerfields import PhoneNumberField


from authentication.validators import (
    validate_otp,
)


USER_MODEL = get_user_model()


class RequestOTPSerializer(serializers.Serializer):
    """
    Serializer درخواست کد تأیید.
    """

    phone_number = PhoneNumberField(
        region="IR",
        required=True,
    )



class VerifyOTPSerializer(serializers.Serializer):
    """
    Serializer تأیید کد یکبار مصرف.
    """

    phone_number = PhoneNumberField(
        region="IR",
        required=True,
    )

    otp = serializers.CharField(
        max_length=6,
        min_length=6,
        trim_whitespace=True,
    )

    def validate_otp(self, value):
        validate_otp(value)
        return value