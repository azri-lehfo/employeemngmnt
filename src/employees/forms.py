from django import forms

from utils.forms import FormExtraClassMixin

from .models import Employee


class EmployeeForm(FormExtraClassMixin, forms.ModelForm):
    """ Add or update Employee form """
    dob = forms.DateField(
        label="Date of Birth",
        required=True,
        widget=forms.TextInput(attrs={
            'placeholder': "dd/mm/yyyy",
            'autocomplete': "off",
            'type': "date"
        })
    )

    class Meta:
        model = Employee
        fields = '__all__'
