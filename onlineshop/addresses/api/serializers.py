from rest_framework import serializers

from addresses.models import Address, Province, City


class ProvinceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Province
        fields = (
            "id",
            "name",
        )



class CitySerializer(serializers.ModelSerializer):
    province = ProvinceSerializer(read_only=True)

    class Meta:
        model = City
        fields = (
            "id",
            "name",
            "province",
        )


class AddressListSerializer(serializers.ModelSerializer):
    province = serializers.CharField(source="province.name", read_only=True)
    city = serializers.CharField(source="city.name", read_only=True)

    class Meta:
        model = Address
        fields = (
            "id",
            "title",
            "receiver_name",
            "receiver_phone",
            "province",
            "city",
            "is_default",
        )



class AddressDetailSerializer(serializers.ModelSerializer):
    province = ProvinceSerializer(read_only=True)
    city = CitySerializer(read_only=True)

    class Meta:
        model = Address
        fields = (
            "id",
            "title",
            "address_type",
            "receiver_name",
            "receiver_phone",
            "province",
            "city",
            "address_line",
            "alley",
            "plaque",
            "unit",
            "postal_code",
            "description",
            "latitude",
            "longitude",
            "is_default",
            "created_at",
            "updated_at",
        )


class AddressCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Address
        fields = (
            "title",
            "address_type",
            "receiver_name",
            "receiver_phone",
            "province",
            "city",
            "address_line",
            "alley",
            "plaque",
            "unit",
            "postal_code",
            "description",
            "latitude",
            "longitude",
        )

    def validate_postal_code(self, value):
        if not value.isdigit() or len(value) != 10:
            raise serializers.ValidationError("کد پستی باید ۱۰ رقم باشد.")
        return value



class AddressUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Address
        fields = (
            "title",
            "address_type",
            "receiver_name",
            "receiver_phone",
            "province",
            "city",
            "address_line",
            "alley",
            "plaque",
            "unit",
            "postal_code",
            "description",
            "latitude",
            "longitude",
        )



