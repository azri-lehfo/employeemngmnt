import uuid

from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

from auths.middleware import get_current_user


class BaseModelMixin(models.Model):
    """
    Base Model must have all these fields
    """
    uuid = models.UUIDField(
        verbose_name=_("UUID Identifier"),
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        help_text=_("Requried, PrimaryKey none-editable"),
        db_index=True,
    )

    created_by = models.ForeignKey(
        User,
        verbose_name=_("Created by"),
        related_name='%(app_label)s_%(class)s_created_by',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        editable=False
    )
    updated_by = models.ForeignKey(
        User,
        verbose_name=_("Updated by"),
        related_name='%(app_label)s_%(class)s_modified_by',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        editable=False
    )

    created_at = models.DateTimeField(
        verbose_name=_("Created at"),
        auto_now=False,
        auto_now_add=True,
        db_index=True
    )
    updated_at = models.DateTimeField(
        verbose_name=_("Updated at"),
        auto_now=True,
        auto_now_add=False,
        db_index=True
    )

    class Meta:
        abstract = True

    def __str__(self):
        return f"{self.uuid}"

    def header_display(self):
        return self.__str__()

    def save(self, *args, **kwargs):
        """
        Overwritting save to ensure the created_by is automatically populated
        """
        try:
            _created_by = User.objects.get(pk=self.created_by_id)
        except User.DoesNotExist:
            _created_by = None

        if self._state.adding and _created_by is None:
            self.created_by = get_current_user()
        self.updated_by = get_current_user()
        super().save(*args, **kwargs)
