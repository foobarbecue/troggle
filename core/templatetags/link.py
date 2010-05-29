from django import template
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter()
def link(value):
    return mark_safe("<a href=\'%s\'>"%value.get_absolute_url()+unicode(value)+"</a>")

