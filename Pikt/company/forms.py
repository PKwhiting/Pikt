from django import forms
from Authentication.models import User
from .models import Company

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'phone_number', 'role', 'password']
        labels = {
            'username': False,
            'first_name': False,
            'last_name': False,
            'email': False,
            'phone_number': False,
            'role': False,
            'password': False,
        }
        help_texts = {
            'username': '',
            'first_name': '',
            'last_name': '',
            'email': '',
            'phone_number': '',
            'role': '',
            'password': '',
        }
        widgets = {
            'username': forms.TextInput(attrs={'class': 'text-field w-input', 'style': 'width: 100%; margin-top: 8px;', 'placeholder': 'Username'}),
            'first_name': forms.TextInput(attrs={'class': 'text-field w-input', 'style': 'width: 100%; margin-top: 8px;', 'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'class': 'text-field w-input', 'style': 'width: 100%; margin-top: 8px;', 'placeholder': 'Last Name'}),
            'email': forms.EmailInput(attrs={'class': 'text-field w-input', 'style': 'width: 100%; margin-top: 8px;', 'placeholder': 'Email Address'}),
            'phone_number': forms.TextInput(attrs={'class': 'text-field w-input', 'style': 'width: 100%; margin-top: 8px;', 'placeholder': 'Phone Number'}),
            'role': forms.Select(attrs={'class': 'text-field', 'style': 'width: 100%; height: 37px;'}),
            'password': forms.PasswordInput(attrs={'class': 'text-field w-input', 'style': 'width: 100%; margin-top: 8px;', 'placeholder': 'Password'}),
        }

    def save(self, commit=True):
        user = super(UserForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user

class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ['name', 'address_line1', 'address_line2', 'city', 'state', 'zip_code', 'phone_number', 'email', 'logo', 'website']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'text-field w-input', 'style': 'width: 100%; margin-top: 8px;', 'placeholder': 'Company Name'}),
            'address_line1': forms.TextInput(attrs={'class': 'text-field w-input', 'style': 'width: 100%; margin-top: 8px;', 'placeholder': 'Address Line 1'}),
            'address_line2': forms.TextInput(attrs={'class': 'text-field w-input', 'style': 'width: 100%; margin-top: 8px;', 'placeholder': 'Address Line 2'}),
            'city': forms.TextInput(attrs={'class': 'text-field w-input', 'style': 'width: 100%; margin-top: 8px;', 'placeholder': 'City'}),
            'state': forms.Select(attrs={'class': 'text-field w-input', 'style': 'width: 100%; margin-top: 8px;'}),
            'zip_code': forms.TextInput(attrs={'class': 'text-field w-input', 'style': 'width: 100%; margin-top: 8px;', 'placeholder': 'Zip Code'}),
            'phone_number': forms.TextInput(attrs={'class': 'text-field w-input', 'style': 'width: 100%; margin-top: 8px;', 'placeholder': 'Phone Number'}),
            'email': forms.EmailInput(attrs={'class': 'text-field w-input', 'style': 'width: 100%; margin-top: 8px;', 'placeholder': 'Email'}),
            'logo': forms.FileInput(attrs={'class': 'file-field w-input', 'style': 'width: 100%; margin-top: 8px;'}),
            'website': forms.TextInput(attrs={'class': 'text-field w-input', 'style': 'width: 100%; margin-top: 8px;', 'placeholder': 'Website'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['state'].choices = [('', 'Select State')] + self.fields['state'].choices[1:]
        self.fields['name'].label = "Company Name"
        self.fields['address_line1'].label = "Address Line 1"
        self.fields['address_line2'].label = "Address Line 2"
        self.fields['city'].label = "City"
        self.fields['state'].label = "State"
        self.fields['zip_code'].label = "Zip Code"
        self.fields['phone_number'].label = "Phone Number"
        self.fields['email'].label = "Email"
        self.fields['logo'].label = "Logo"
        self.fields['website'].label = "Website"