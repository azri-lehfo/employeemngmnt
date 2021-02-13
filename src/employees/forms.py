from django import forms

from utils.forms import FormExtraClassMixin

from .models import Employee


class EmployeeForm(FormExtraClassMixin, forms.ModelForm):
    """ Add or update Employee form """

    class Meta:
        model = Employee
        fields = '__all__'
