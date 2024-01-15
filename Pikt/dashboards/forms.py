from django import forms
from .models import part

class PartForm(forms.ModelForm):
    part_image_1 = forms.ImageField(required=False)
    part_image_2 = forms.ImageField(required=False)
    part_image_3 = forms.ImageField(required=False)
    part_image_4 = forms.ImageField(required=False)
    part_image_5 = forms.ImageField(required=False)
    part_image_6 = forms.ImageField(required=False)
    part_image_7 = forms.ImageField(required=False)
    part_image_8 = forms.ImageField(required=False)
    part_image_9 = forms.ImageField(required=False)
    part_image_10 = forms.ImageField(required=False)

    class Meta:
        model = part
        fields = [
            'vehicle_year', 'vehicle_make', 'vehicle_model', 'vehicle_trim', 
            'vehicle_engine', 'vehicle_color', 'part_type', 'part_fitment_location', 
            'part_grade', 'part_interchange', 'part_notes', 'vehicle_fitment', 
            'part_image_1', 'part_image_2', 'part_image_3', 'part_image_4', 
            'part_image_5', 'part_image_6', 'part_image_7', 'part_image_8', 
            'part_image_9', 'part_image_10'
        ]