from django import forms

from utils.forms import FormExtraClassMixin

from .models import Job


class JobForm(FormExtraClassMixin, forms.ModelForm):
    """ Add or update Job form """

    class Meta:
        model = Job
        fields = '__all__'
