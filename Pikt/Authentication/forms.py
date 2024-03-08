from django import forms
from .models import funnelSubmission

class FunnelSubmissionForm(forms.ModelForm):
    YARD_SIZE_CHOICES = [
        ('', 'Select Yard Size...'),
        ('0-500 Vehicles', '0-500 Vehicles'),
        ('500-1000 Vehicles', '500-1000 Vehicles'),
        ('1000+ Vehicles', '1000+ Vehicles'),
    ]
    PAIN_POINT_OPTIONS = [
        ('Managing/Adding Parts Inventory', 'Managing/Adding Parts Inventory'),
        ('Selling Parts', 'Selling Parts'),
        ('Buying/Managing Vehicles', 'Buying/Managing Vehicles'),
        ('Managing Customers', 'Managing Customers'),
        ('Managing invoices/POs', 'Managing Invoices/POs'),
        ('Other', 'Other'),
    ]


    name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Name', 'class': 'text-field w-input'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'Email', 'class': 'text-field w-input'}))
    yard_size = forms.ChoiceField(choices=YARD_SIZE_CHOICES, initial='', widget=forms.Select(attrs={'disabled': 'disabled'}))
    company = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Company', 'class': 'text-field w-input'}))
    message = forms.ChoiceField(required=True, choices=PAIN_POINT_OPTIONS, widget=forms.RadioSelect)
    otherInput = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'text-field w-input', 'style': 'display:none;'}))

    class Meta:
        model = funnelSubmission
        fields = ['name', 'email', 'yard_size', 'company', 'message']
