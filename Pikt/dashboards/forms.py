from django import forms
from .models import Part
from .models import Vehicle, PartPreference
from .const.const import PARTS_CONST


class VehicleForm(forms.ModelForm):
    class Meta:
        model = Vehicle
        fields = '__all__'  # Assuming you want to include all fields from the model

    def __init__(self, *args, **kwargs):
        super(VehicleForm, self).__init__(*args, **kwargs)
        self.fields['user'].required = False

class VehicleFilterForm(forms.ModelForm):

    class Meta:
        model = Vehicle
        fields = ['vin', 'year', 'make', 'model']
        widgets = {
            'vin': forms.TextInput(attrs={'class': 'text-field w-input', 'style': 'width: 100%; margin-top: 8px;', 'placeholder': 'VIN'}),
            'year': forms.TextInput(attrs={'class': 'text-field w-input', 'style': 'width: 100%; margin-top: 8px;', 'placeholder': 'Year'}),
            'make': forms.TextInput(attrs={'class': 'text-field w-input', 'style': 'width: 100%; margin-top: 8px;', 'placeholder': 'Make'}),
            'model': forms.TextInput(attrs={'class': 'text-field w-input', 'style': 'width: 100%; margin-top: 8px;', 'placeholder': 'Model'}),
        }
        # labels = {
        #     'stock_number': '',
        #     'year': '',
        #     'make': '',
        #     'model': '',
        # }
        # required = {
        #     'year': False,
        #     'make': False,
        #     'model': False
        # }
    def set_values(self):
        print("TACOS")

class PartForm(forms.ModelForm):
    image_1 = forms.ImageField(required=False)
    image_2 = forms.ImageField(required=False)
    image_3 = forms.ImageField(required=False)
    image_4 = forms.ImageField(required=False)
    image_5 = forms.ImageField(required=False)
    image_6 = forms.ImageField(required=False)
    image_7 = forms.ImageField(required=False)
    image_8 = forms.ImageField(required=False)
    image_9 = forms.ImageField(required=False)
    image_10 = forms.ImageField(required=False)

    class Meta:
        model = Part
        fields = '__all__'
    def clean(self):
        cleaned_data = super().clean()
        vehicle_fitments = self.get_fitment()
        cleaned_data['vehicle_fitment'] = vehicle_fitments
        weight_in_ounces = self.get_weight_in_ounces()
        cleaned_data['weight'] = weight_in_ounces
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

class PartPreferenceForm(forms.ModelForm):
    parts = forms.MultipleChoiceField(
        choices=[(part, part) for part in PARTS_CONST],
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label=''
    )

    class Meta:
        model = PartPreference
        fields = ['parts']

    def __init__(self, *args, **kwargs):
        initial = kwargs.get('initial', {})
        if 'parts' not in initial:
            if 'instance' in kwargs and kwargs['instance']:
                initial['parts'] = kwargs['instance'].get_parts_list()
        kwargs['initial'] = initial
        super().__init__(*args, **kwargs)
        # Set initial for the parts field explicitly
        if 'parts' in self.fields:
            self.fields['parts'].initial = initial.get('parts', [])

    def save(self, commit=True):
        instance = super().save(commit=False)
        print("--============-0))))0")
        print(self.cleaned_data)
        instance.set_parts_list(self.cleaned_data['parts'])
        if commit:
            instance.save()
        return instance
    
from .models import PART_GRADES
class PartForm(forms.ModelForm):
    class Meta:
        model = Part
        fields = ['type', 'stock_number', 'price', 'description', 'location', 'grade']
        widgets = {
            'type': forms.TextInput(attrs={'Placeholder': 'Type', 'class': 'text-field w-input', 'readonly': 'readonly', 'style': 'width: 90%; margin-top: 8px;'}),
            'stock_number': forms.TextInput(attrs={'Placeholder': 'Type', 'class': 'text-field w-input', 'readonly': 'readonly', 'style': 'width: 90%; margin-top: 8px;'}),
            'price': forms.NumberInput(attrs={'class': 'text-field w-input', 'style': 'width: 90%; margin-top: 8px;', 'step': '0.5', 'value': '0.00'}),
            'description': forms.TextInput(attrs={'Placeholder': 'Description', 'class': 'text-field w-input', 'style': 'width: 90%; margin-top: 8px;'}),
            'location': forms.TextInput(attrs={'Placeholder': 'Location', 'class': 'text-field w-input', 'style': 'width: 90%; margin-top: 8px;'}),
            'grade': forms.Select(attrs={'class': 'text-field w-select', 'style': 'width: 90%; margin-top: 8px;'}),
        }
        labels = {
            'type': '',
            'stock_number': '',
            'price': '',
            'description': '',
            'location': '',
            'grade': '',
        }

class VehicleForm(forms.ModelForm):
    class Meta:
        model = Vehicle
        fields = ['vin', 'year', 'make', 'model', 'trim']