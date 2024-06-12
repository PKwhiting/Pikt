from datetime import datetime
from django import template
from django.utils import timezone
from dashboards.models import Vehicle

register = template.Library()

@register.filter
def days_since(value):
    diff = timezone.now() - value
    return int(diff.days)

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

@register.filter
def getattribute(obj, attr):
    return getattr(obj, attr, None)

@register.filter
def model_fields(obj):
    fields = []
    for field in obj._meta.fields:
        if 'image' not in field.name and '_' not in field.name and field.name != 'id' and field.name != 'vehicle':
            field_name = field.name
            field_value = getattr(obj, field_name)
            fields.append({'name': field_name, 'value': field_value})
    return fields