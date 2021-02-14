import uuid

from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType


class Log(models.Model):
    """
    Log for user view activities
    """
    uuid = models.UUIDField(
        verbose_name=_("UUID Identifier"),
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        help_text=_("Requried, PrimaryKey none-editable"),
        db_index=True,
    )
    user = models.ForeignKey(
        User,
        verbose_name=_("Created by"),
        on_delete=models.CASCADE,
        editable=False
    )
    employee_model = models.Q(app_label='employees', model='employee')
    job_model = models.Q(app_label='jobs', model='job')
    limited_models = (
        employee_model
        | job_model
    )
    content_type = models.ForeignKey(
        ContentType,
        limit_choices_to=limited_models,
        on_delete=models.CASCADE,
        verbose_name=_("Content Type")
    )
    object_id = models.UUIDField(verbose_name=_("Object ID"))
    content_object = GenericForeignKey()

    created_at = models.DateTimeField(
        verbose_name=_("Created at"),
        auto_now=False,
        auto_now_add=True,
        db_index=True
    )
