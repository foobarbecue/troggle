from django.template.defaultfilters import stringfilter
from django import template

register = template.Library()

@register.filter
@stringfilter
def none2nan(value):
    "Removes all values of arg from the given string"
    return value.replace('None', 'NaN')

