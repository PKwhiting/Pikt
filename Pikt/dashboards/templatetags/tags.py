from django import template
from django.utils import timezone

register = template.Library()

@register.filter
def days_since(value):
    diff = timezone.now() - value
    return int(diff.days)

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)