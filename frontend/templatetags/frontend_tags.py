from django import template

register = template.Library()

@register.filter
def percentage(val):
    return val * 100

@register.filter
def thousands(val):
    return '{:,}'.format(val).replace(',','.')
