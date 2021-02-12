from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType

from .models import Log


def create_view_log(
    user: User,
    obj
) -> Log:
    """
    Service to store view logs.
    """
    content_type = ContentType.objects.get_for_model(obj),
    object_id = obj.pk
    log = Log.objects.create(
        user=user,
        content_type=content_type,
        object_id=object_id
    )
    return log
