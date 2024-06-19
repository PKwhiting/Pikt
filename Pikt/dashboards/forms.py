from django import forms
from .models import Part
from .models import Vehicle, PartPreference, Customer
from .const.const import PARTS_CONST, STATE_CHOICES



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
        fields = ['vin', 'year', 'make', 'model', 'trim', 'location']
        widgets = {
            'vin': forms.TextInput(attrs={'class': 'text-field w-input', 'style': 'width: 100%; margin-top: 8px;', 'placeholder': 'VIN'}),
            'year': forms.TextInput(attrs={'class': 'text-field w-input', 'style': 'width: 100%; margin-top: 8px;', 'placeholder': 'Year'}),
            'make': forms.TextInput(attrs={'class': 'text-field w-input', 'style': 'width: 100%; margin-top: 8px;', 'placeholder': 'Make'}),
            'model': forms.TextInput(attrs={'class': 'text-field w-input', 'style': 'width: 100%; margin-top: 8px;', 'placeholder': 'Model'}),
            'trim': forms.TextInput(attrs={'class': 'text-field w-input', 'style': 'width: 100%; margin-top: 8px;', 'placeholder': 'Trim'}),
            'location': forms.TextInput(attrs={'class': 'text-field w-input', 'style': 'width: 100%; margin-top: 8px;', 'placeholder': 'Location'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['vin'].label = ""
        self.fields['year'].label = ""
        self.fields['make'].label = ""
        self.fields['model'].label = ""
        self.fields['trim'].label = ""
        self.fields['location'].label = ""

class PartFilterForm(forms.ModelForm):

    class Meta:
        model = Part
        fields = ['stock_number', 'type', 'location', 'grade', 'ebay_listed', 'marketplace_listed']
        widgets = {
            'stock_number': forms.TextInput(attrs={'class': 'text-field w-input', 'style': 'width: 100%; margin-top: 8px;', 'placeholder': 'Stock Number'}),
            'type': forms.TextInput(attrs={'class': 'text-field w-input', 'style': 'width: 100%; margin-top: 8px;', 'placeholder': 'Part Type'}),
            'location': forms.TextInput(attrs={'class': 'text-field w-input', 'style': 'width: 100%; margin-top: 8px;', 'placeholder': 'Location'}),
            'grade': forms.Select(attrs={'class': 'text-field w-input', 'style': 'width: 100%; margin-top: 8px;', 'placeholder': 'Part Grade'}, choices=[('Part Grade','Part Grade')]),
            'ebay_listed': forms.CheckboxInput(attrs={'class': 'switch', 'style': 'width: 100%; margin-top: 8px;', 'placeholder': 'Ebay Listed'}),
            'marketplace_listed': forms.CheckboxInput(attrs={'class': 'switch', 'style': 'width: 100%; margin-top: 8px;'}),
        }
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields['location'].label = ""
            self.fields['stock_number'].label = ""
            self.fields['type'].label = ""
            self.fields['grade'].label = ""
            self.fields['ebay_listed'].label = "Ebay"
            self.fields['marketplace_listed'].label = "Facebook Marketplace"

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
            'grade': forms.Select(attrs={'class': 'text-field w-input', 'style': 'width: 90%; margin-top: 8px;'}),
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

class EditPartForm(forms.ModelForm):
    class Meta:
        model = Part
        fields = ['type', 'stock_number', 'price', 'description', 'location', 'grade', 'interchange', 'part_number', 'ebay_listed', 'mercari_listed', 'marketplace_listed', 'sold']
        widgets = {
            'type': forms.TextInput(attrs={'placeholder': 'Type', 'class': 'text-field w-input'}),
            'stock_number': forms.TextInput(attrs={'placeholder': 'Stock Number', 'class': 'text-field w-input'}),
            'price': forms.TextInput(attrs={'placeholder': 'Price', 'class': 'text-field w-input'}),
            'description': forms.TextInput(attrs={'placeholder': 'Description', 'class': 'text-field w-input'}),
            'location': forms.TextInput(attrs={'placeholder': 'Location', 'class': 'text-field w-input'}),
            'grade': forms.Select(attrs={'class': 'text-field w-input'} ),
            'interchange': forms.TextInput(attrs={'placeholder': 'Interchange', 'class': 'text-field w-input'}),
            'part_number': forms.TextInput(attrs={'placeholder': 'Part Number', 'class': 'text-field w-input'}),
            'ebay_listed': forms.CheckboxInput(attrs={'class': 'text-field w-checkbox'}),
            'mercari_listed': forms.CheckboxInput(attrs={'class': 'text-field w-checkbox'}),
            'marketplace_listed': forms.CheckboxInput(attrs={'class': 'text-field w-checkbox'}),
            'sold': forms.CheckboxInput(attrs={'class': 'text-field w-checkbox'}),
        }

class EditVehicleForm(forms.ModelForm):
    class Meta:
        model = Vehicle
        fields = ['vin', 'year', 'make', 'model', 'trim', 'location', 'engine', 'mileage', 'transmission', 'body_type', 'drivetrain', 'primary_damage', 'secondary_damage']
        widgets = {
            'vin': forms.TextInput(attrs={'Placeholder': 'VIN', 'class': 'text-field w-input'}),
            'year': forms.TextInput(attrs={'Placeholder': 'Year', 'class': 'text-field w-input'}),
            'make': forms.TextInput(attrs={'Placeholder': 'Make', 'class': 'text-field w-input'}),
            'model': forms.TextInput(attrs={'Placeholder': 'Model', 'class': 'text-field w-input'}),
            'trim': forms.TextInput(attrs={'Placeholder': 'Trim', 'class': 'text-field w-input'}),
            'location': forms.TextInput(attrs={'Placeholder': 'Location', 'class': 'text-field w-input'}),
            'engine': forms.TextInput(attrs={'Placeholder': 'Engine', 'class': 'text-field w-input'}),
            'mileage': forms.TextInput(attrs={'Placeholder': 'Mileage', 'class': 'text-field w-input'}),
            'transmission': forms.TextInput(attrs={'Placeholder': 'Transmission', 'class': 'text-field w-input'}),
            'body_type': forms.TextInput(attrs={'Placeholder': 'Body Type', 'class': 'text-field w-input'}),
            'drivetrain': forms.TextInput(attrs={'Placeholder': 'Drivetrain', 'class': 'text-field w-input'}),
            'primary_damage': forms.TextInput(attrs={'Placeholder': 'Primary Damage', 'class': 'text-field w-input'}),
            'secondary_damage': forms.TextInput(attrs={'Placeholder': 'Secondary Damage', 'class': 'text-field w-input'}),
        }

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['name', 'owner', 'address', 'city', 'state', 'zip_code', 'phone', 'email']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'text-field w-input', 'style': 'width: 100%; margin-top: 8px;', 'placeholder': 'Customer Name'}),
            'owner': forms.TextInput(attrs={'class': 'text-field w-input', 'style': 'width: 100%; margin-top: 8px;', 'placeholder': 'Owner Name'}),
            'address': forms.TextInput(attrs={'class': 'text-field w-input', 'style': 'width: 100%; margin-top: 8px;', 'placeholder': 'Address'}),
            'city': forms.TextInput(attrs={'class': 'text-field w-input', 'style': 'width: 100%; margin-top: 8px;', 'placeholder': 'City'}),
            'state': forms.Select(attrs={'class': 'text-field w-input',} ),
            'zip_code': forms.TextInput(attrs={'class': 'text-field w-input', 'style': 'width: 100%; margin-top: 8px;', 'placeholder': 'Zip Code'}),
            'phone': forms.TextInput(attrs={'class': 'text-field w-input', 'style': 'width: 100%; margin-top: 8px;', 'placeholder': 'Phone'}),
            'email': forms.EmailInput(attrs={'class': 'text-field w-input', 'style': 'width: 100%; margin-top: 8px;', 'placeholder': 'Email'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].label = ""
        self.fields['name'].required = True

        self.fields['owner'].label = ""

        self.fields['address'].label = ""
        self.fields['address'].required = True

        self.fields['city'].label = ""
        self.fields['city'].required = True

        self.fields['state'].label = ""
        self.fields['state'].required = True
        self.fields['state'].choices = [('', 'Select State')] + self.fields['state'].choices[1:]

        self.fields['zip_code'].required = True
        self.fields['zip_code'].label = ""

        self.fields['phone'].required = True
        self.fields['phone'].label = ""

        self.fields['email'].label = ""
