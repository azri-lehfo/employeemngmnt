from decimal import Decimal

from django import forms
from django.utils.translation import gettext_lazy as _

from utils.forms import FormExtraClassMixin

from .models import Job


class JobForm(FormExtraClassMixin, forms.ModelForm):
    """ Add or update Job form """

    description = forms.CharField(
        widget=forms.Textarea(attrs={
            'rows': 3
        })
    )

    class Meta:
        model = Job
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()

        if any(self._errors):
            return cleaned_data

        if Decimal(cleaned_data.get('max_salary', '0.0')) <= Decimal(cleaned_data.get('min_salary', '0.0')):
            self.add_error('max_salary', _("Max salary must be larger than min salary."))

        return cleaned_data
