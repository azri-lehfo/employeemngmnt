from django.contrib.auth.models import User

from .models import Log


def create_view_log(
    user: User,
    page: str
) -> Log:
    """
    Service to store view logs.
    """
    log = Log.objects.create(
        user=user,
        page=page
    )
    return log
