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
    value = getattr(obj, attr, None)
    if attr in ['ebay_listed', 'mercari_listed', 'marketplace_listed']:
        if value == False:
            return '<div class="status"><div class="indication-color bg-primary-orange"></div><div>False</div></div>'
        elif value == True:
            return '<div class="status"><div class="indication-color bg-primary-green"></div><div>Listed</div></div>'
    else:
        return value
    

@register.filter
def model_fields(obj):
    fields = []
    for field in obj._meta.fields:
        if 'image' not in field.name and field.name != 'id' and field.name != 'vehicle':
            field_name = field.name.replace('_', ' ')
            field_value = getattr(obj, field.name)
            fields.append({'name': field_name, 'value': field_value})
    return fields

@register.filter
def custom_switch(field):
    return '''
        <label class="w-checkbox switch-field" style="margin-right: auto; margin-left: auto;">
            <input id="{id}" type="checkbox" class="switch" name="{name}" value="{value}" {checked}>
            <span class="checkbox-label w-form-label" for="{id}" style="margin-left: 5px;">
                <div>{label}</div>
            </span>
        </label>
    '''.format(
        id=field.auto_id if hasattr(field, 'auto_id') else '',
        name=field.html_name if hasattr(field, 'html_name') else '',
        value=field.value() if hasattr(field, 'value') and field.value() is not None else '',
        checked='checked' if hasattr(field, 'value') and field.value() else '',
        label=field.label if hasattr(field, 'label') else ''
    )