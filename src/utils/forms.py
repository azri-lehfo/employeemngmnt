from django import forms


class FormExtraClassMixin(object):
    """
    Control the class here
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for name, field in self.fields.items():

            added_class = 'form-control'

            original_attributes = field.widget.attrs.get('class')

            if original_attributes:
                added_class += f" {original_attributes}"

            if isinstance(field, forms.DateField):
                added_class += " datepicker"

            if isinstance(field.widget, forms.widgets.Select):
                added_class += " core-select2"

            # Add all the new attributes to the class.
            self.fields[name].widget.attrs['class'] = added_class
            self.fields[name].widget.attrs['placeholder'] = name.title().replace("_", " ")

            # set all textarea to 3 rows
            if isinstance(field.widget, forms.widgets.Textarea):
                self.fields[name].widget.attrs['rows'] = 3
