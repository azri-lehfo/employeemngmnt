from django.db import models
from django.utils.translation import gettext_lazy as _

from utils.models import BaseModelMixin


class Employee(BaseModelMixin):
    """
    Store employee details.
    """
    name = models.CharField(
        verbose_name=_("Name"),
        help_text=_("Required."),
        max_length=255,
    )
    dob = models.DateField(
        verbose_name=_("Date of Birth"),
        help_text=_("Pick a Date.")
    )
    salary = models.DecimalField(
        verbose_name=_("Salary"),
        default=0.00,
        max_digits=12,
        decimal_places=2
    )
    job = models.ForeignKey(
        'jobs.Job',
        related_name='jobs',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )

    def __str__(self):
        return f"{self.name}"
