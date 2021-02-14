import uuid

from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _


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
    page = models.CharField(
        verbose_name=_("Page"),
        help_text=_("Required."),
        max_length=255,
    )

    created_at = models.DateTimeField(
        verbose_name=_("Created at"),
        auto_now=False,
        auto_now_add=True,
        db_index=True
    )
