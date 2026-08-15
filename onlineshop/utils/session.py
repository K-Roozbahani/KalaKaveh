def get_session_key(request):
    """
    دریافت Session Key درخواست.

    در صورت نداشتن Session Key، یک Session جدید ایجاد می‌شود.
    """

    if request.session.session_key is None:
        request.session.create()

    return request.session.session_key