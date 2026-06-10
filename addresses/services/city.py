from addresses.models import City, Province


# ----------------------------
# Get all provinces
# ----------------------------
def get_provinces():
    """
    دریافت لیست استان‌ها
    مناسب برای فرم‌ها و API
    """

    return Province.objects.all()

# ----------------------------
# Get cities by province
# ----------------------------
def get_cities_by_province(*, province: Province):
    """
    دریافت شهرهای یک استان
    برای dropdown وابسته (Cascading Select)
    """

    return City.objects.filter(province=province)

# ----------------------------
# Get city by id (safe lookup)
# ----------------------------
def get_city_by_id(*, city_id: int):
    """
    گرفتن یک شهر با id
    """

    return City.objects.filter(id=city_id).first()

# ----------------------------
# Validate city belongs to province
# ----------------------------
def validate_city_belongs_to_province(*, city: City, province: Province) -> bool:
    """
    بررسی اینکه شهر متعلق به استان هست یا نه
    """

    return city.province_id == province.id

