from django import forms
from .models import funnelSubmission

class FunnelSubmissionForm(forms.ModelForm):
    YARD_SIZE_CHOICES = [
        ('', 'Select Yard Size...'),
        ('0-500 Vehicles', '0-500 Vehicles'),
        ('500-1000 Vehicles', '500-1000 Vehicles'),
        ('1000+ Vehicles', '1000+ Vehicles'),
    ]

    name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Name', 'class': 'text-field w-input'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'Email', 'class': 'text-field w-input'}))
    yard_size = forms.ChoiceField(choices=YARD_SIZE_CHOICES, initial='', widget=forms.Select(attrs={'disabled': 'disabled'}))
    company = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Company', 'class': 'text-field w-input'}))

    yard_size = forms.ChoiceField(choices=YARD_SIZE_CHOICES)

    class Meta:
        model = funnelSubmission
        fields = ['name', 'email', 'yard_size', 'company']