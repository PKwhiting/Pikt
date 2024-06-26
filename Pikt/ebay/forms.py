from django import forms
from .models import EbayPolicy, EbayMIPCredentials
import uuid


class EbayPolicyForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['policy_type'].widget.attrs['readonly'] = True
        self.fields['policy_name'].required = True
        self.fields['policy_type'].required = True
        self.fields['policy_type'].widget.attrs['id'] = f'policy_type_{uuid.uuid4().hex[:6]}'
        self.fields['policy_name'].widget.attrs['id'] = f'policy_name_{uuid.uuid4().hex[:6]}'

    class Meta:
        model = EbayPolicy
        fields = '__all__'
        widgets = {
            'company': forms.Select(attrs={'class': 'w-input'}),
            'policy_type': forms.TextInput(attrs={'class': 'w-input text-field', 'readonly': 'readonly', 'required': 'required'}),
            'policy_name': forms.TextInput(attrs={'class': 'w-input text-field', 'placeholder': 'Policy Name', 'required': 'required'}),
        }

class EbayMIPCredentialsForm(forms.ModelForm):
    class Meta:
        model = EbayMIPCredentials
        fields = '__all__'
        widgets = {
            'username': forms.TextInput(attrs={'class': 'w-input text-field', 'placeholder': 'Username', 'required': 'required'}),
            'password': forms.TextInput(attrs={'class': 'w-input text-field', 'placeholder': 'Password', 'required': 'required'}),
        }




