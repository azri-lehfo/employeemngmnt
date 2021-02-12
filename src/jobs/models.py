from django.db import models
from django.utils.translation import gettext_lazy as _

from utils.models import BaseModelMixin


class Job(BaseModelMixin):
    """
    Store job details.
    """
    title = models.CharField(
        verbose_name=_("Name"),
        help_text=_("Required."),
        max_length=255,
    )
    description = models.CharField(
        verbose_name=_("Description"),
        max_length=255,
        help_text=_("Required, Maximum of 255 Characters.")
    )
    min_salary = models.DecimalField(
        verbose_name=_("Minimum Salary"),
        default=0.00,
        max_digits=12,
        decimal_places=2
    )
    max_salary = models.DecimalField(
        verbose_name=_("Maximum Salary"),
        default=0.00,
        max_digits=12,
        decimal_places=2
    )

    def __str__(self):
        return f"{self.title}"
