from django import template

register = template.Library()


@register.simple_tag
def define(obj):
    """
    Use in the Templates with `{% define var as new_var %}`
    """
    return obj
