from django import forms
from .models import part
from .models import Vehicle


class VehicleForm(forms.ModelForm):
    class Meta:
        model = Vehicle
        fields = '__all__'  # Assuming you want to include all fields from the model

    def __init__(self, *args, **kwargs):
        super(VehicleForm, self).__init__(*args, **kwargs)
        self.fields['user'].required = False


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
            'vehicle_engine', 'vehicle_color', 'type', 'fitment_location', 
            'grade', 'hollander_interchange', 'length', 'width', 'height', 'notes', 'cost', 'price',
            'part_image_1', 'part_image_2', 'part_image_3', 'part_image_4', 
            'part_image_5', 'part_image_6', 'part_image_7', 'part_image_8', 
            'part_image_9', 'part_image_10'
        ]
    def clean(self):
        cleaned_data = super().clean()
        vehicle_fitments = self.get_fitment()
        cleaned_data['vehicle_fitment'] = vehicle_fitments
        part_weight_in_ounces = self.get_weight_in_ounces()
        cleaned_data['weight'] = part_weight_in_ounces
        return cleaned_data
    
    def get_weight_in_ounces(self):
        ounces = self.data.get('ozs')
        pounds = self.data.get('lbs')
        ounces = int(ounces) if ounces else 0
        pounds = int(pounds) if pounds else 0
        ounces += pounds * 16
        return ounces

    def get_fitment(self):
        vehicle_fitments = {}
        for key in self.data:
            if key.startswith('vehicle_make_fitment_'):
                index = key.split('_')[-1]
                model_field = f'vehicle_model_fitment_{index}'
                year_field = f'vehicle_year_fitment_{index}'
                make = self.data.get(key)
                model = self.data.get(model_field)
                years = self.data.getlist(year_field)
                vehicle_fitments[index] = {
                    'make': make,
                    'model': model,
                    'year': years
                }
        return vehicle_fitments

